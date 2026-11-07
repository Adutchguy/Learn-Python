// Talks to the Pyodide web worker (public/pyodide-worker.js).
// If a program runs too long, or the learner presses Stop, the worker is terminated and a fresh
// one is started: that is the only reliable way to interrupt a runaway Python loop in a browser.

export interface PythonConfig {
  workerUrl: string;
  indexURL: string; // folder of the Pyodide distribution, ending with "/"
  runnerUrl: string; // URL of py/learn_runner.py
  packages?: string[]; // Pyodide packages to load at start-up (for example "numpy", "pandas")
}

export interface RunResult {
  output: string;
  error: string | null;
}

export interface TestResult {
  name: string;
  passed: boolean;
  message: string;
}

export type Status = "loading" | "ready" | "busy" | "error";

export class StoppedError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "StoppedError";
  }
}

interface Pending {
  resolve: (value: unknown) => void;
  reject: (reason: Error) => void;
  timer: ReturnType<typeof setTimeout>;
}

const LOAD_TIMEOUT_MS = 90_000;
// Downloading packages such as pandas can take much longer on a slow connection.
const LOAD_TIMEOUT_WITH_PACKAGES_MS = 240_000;

export class PythonClient {
  onStatus: (status: Status, detail?: string) => void = () => {};

  private worker: Worker | null = null;
  private ready: Promise<void> = Promise.resolve();
  private pending = new Map<number, Pending>();
  private nextId = 1;

  constructor(private config: PythonConfig) {}

  /** Start loading Python in the background. Safe to call more than once. */
  start(): Promise<void> {
    if (this.worker) return this.ready;
    return this.spawn();
  }

  run(source: string, stdin: string, timeoutMs = 10_000): Promise<RunResult> {
    return this.request("run", { source, stdin }, timeoutMs) as Promise<RunResult>;
  }

  test(source: string, tests: string, timeoutMs = 20_000): Promise<TestResult[]> {
    return this.request("test", { source, tests }, timeoutMs) as Promise<TestResult[]>;
  }

  /** Abort whatever is running (if anything) and get a fresh interpreter. */
  stop(reason = "Stopped."): void {
    this.failAll(new StoppedError(reason));
    this.spawn();
  }

  private spawn(): Promise<void> {
    this.worker?.terminate();
    const worker = new Worker(this.config.workerUrl, { type: "module" });
    this.worker = worker;
    this.onStatus("loading");

    this.ready = new Promise<void>((resolve, reject) => {
      const timer = setTimeout(
        () => fail(new Error("Python took too long to load. Check your connection and reload the page.")),
        this.config.packages?.length ? LOAD_TIMEOUT_WITH_PACKAGES_MS : LOAD_TIMEOUT_MS,
      );
      const fail = (error: Error) => {
        clearTimeout(timer);
        if (this.worker === worker) this.onStatus("error", error.message);
        reject(error);
      };
      worker.addEventListener("message", (event: MessageEvent) => {
        const msg = event.data;
        if (this.worker !== worker) return; // a stale worker
        if (msg.type === "ready") {
          clearTimeout(timer);
          this.onStatus("ready");
          resolve();
        } else if (msg.type === "init-error") {
          fail(new Error(msg.error));
        } else if (msg.type === "result") {
          this.settle(msg);
        }
      });
      worker.addEventListener("error", (event) => {
        fail(new Error(event.message || "The Python worker failed to start."));
      });
      worker.postMessage({
        type: "init",
        indexURL: this.config.indexURL,
        runnerUrl: this.config.runnerUrl,
        packages: this.config.packages ?? [],
      });
    });
    this.ready.catch(() => {}); // errors are reported through onStatus and request()
    return this.ready;
  }

  private async request(type: "run" | "test", payload: Record<string, string>, timeoutMs: number): Promise<unknown> {
    await this.start();
    await this.ready;
    const worker = this.worker;
    if (!worker) throw new Error("Python is not running.");
    const id = this.nextId++;
    this.onStatus("busy");
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        this.failAll(
          new StoppedError(`That took longer than ${Math.round(timeoutMs / 1000)} seconds, so it was stopped. Is a loop never ending?`),
        );
        this.spawn();
      }, timeoutMs);
      this.pending.set(id, { resolve, reject, timer });
      worker.postMessage({ type, id, ...payload });
    });
  }

  private settle(msg: { id: number; ok: boolean; result?: unknown; error?: string }): void {
    const pending = this.pending.get(msg.id);
    if (!pending) return;
    this.pending.delete(msg.id);
    clearTimeout(pending.timer);
    if (this.pending.size === 0) this.onStatus("ready");
    if (msg.ok) pending.resolve(msg.result);
    else pending.reject(new Error(msg.error || "Something went wrong while running Python."));
  }

  private failAll(error: Error): void {
    for (const pending of this.pending.values()) {
      clearTimeout(pending.timer);
      pending.reject(error);
    }
    this.pending.clear();
  }
}
