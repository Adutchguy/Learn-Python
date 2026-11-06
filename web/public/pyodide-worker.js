/*
 * Web Worker that hosts Pyodide, so a slow or endless learner program never freezes the page.
 * The page can terminate this worker at any time (Stop button / timeout) and start a new one.
 *
 * This is a *module* worker (new Worker(url, { type: "module" })): current Pyodide releases
 * no longer support classic workers, so Pyodide is loaded from its pyodide.mjs file.
 *
 * Protocol (messages to the worker):
 *   { type: "init", indexURL, runnerUrl }
 *   { type: "run",  id, source, stdin }
 *   { type: "test", id, source, tests }
 * Messages from the worker:
 *   { type: "ready" } | { type: "init-error", error }
 *   { type: "result", id, ok: true, result } | { type: "result", id, ok: false, error }
 */
import "./runner-core.js";

let runner = null;

self.onmessage = async (event) => {
  const msg = event.data;
  try {
    if (msg.type === "init") {
      const { loadPyodide } = await import(msg.indexURL + "pyodide.mjs");
      const pyodide = await loadPyodide({ indexURL: msg.indexURL });
      const response = await fetch(msg.runnerUrl);
      if (!response.ok) throw new Error("Could not load the Python runner (" + response.status + ")");
      runner = self.LearnRunner.create(pyodide, await response.text());
      self.postMessage({ type: "ready" });
    } else if (msg.type === "run" || msg.type === "test") {
      if (!runner) throw new Error("Python is not ready yet");
      const result =
        msg.type === "run" ? runner.runProgram(msg.source, msg.stdin) : runner.runTests(msg.source, msg.tests);
      self.postMessage({ type: "result", id: msg.id, ok: true, result: result });
    }
  } catch (err) {
    const text = String((err && err.message) || err);
    if (msg.type === "init") self.postMessage({ type: "init-error", error: text });
    else self.postMessage({ type: "result", id: msg.id, ok: false, error: text });
  }
};
