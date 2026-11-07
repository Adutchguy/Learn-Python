// Registers the service worker (production builds only) and powers the "Download for offline"
// button on the home page, which saves Python itself for use without a connection.
export const PYODIDE_CACHE = "lp-pyodide";
const CORE_FILES = ["pyodide.mjs", "pyodide-lock.json", "pyodide.asm.mjs", "pyodide.asm.wasm", "python_stdlib.zip"];

if (import.meta.env.PROD && "serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker.register(import.meta.env.BASE_URL.replace(/\/?$/, "/") + "sw.js").catch(() => {
      /* Offline support is a bonus; the site works without it. */
    });
  });
}

type LockFile = { packages: Record<string, { file_name: string; depends?: string[] }> };

/** The files needed for the given Pyodide packages, including everything they depend on. */
export function packageFiles(lock: LockFile, names: string[]): string[] {
  const seen = new Set<string>();
  const files: string[] = [];
  const visit = (name: string) => {
    const key = name.toLowerCase().replace(/_/g, "-");
    if (seen.has(key)) return;
    seen.add(key);
    const entry = lock.packages[key];
    if (!entry) return;
    files.push(entry.file_name);
    (entry.depends ?? []).forEach(visit);
  };
  names.forEach(visit);
  return files;
}

async function isDownloaded(base: string): Promise<boolean> {
  if (!("caches" in window)) return false;
  const cache = await caches.open(PYODIDE_CACHE);
  const checks = await Promise.all(CORE_FILES.map((f) => cache.match(base + f)));
  return checks.every(Boolean);
}

async function download(base: string, packages: string[], onProgress: (done: number, total: number) => void) {
  const cache = await caches.open(PYODIDE_CACHE);
  const lockResponse = await fetch(base + "pyodide-lock.json");
  if (!lockResponse.ok) throw new Error(`Could not reach the Python download (${lockResponse.status}).`);
  await cache.put(base + "pyodide-lock.json", lockResponse.clone());
  const lock = (await lockResponse.json()) as LockFile;
  const files = [...CORE_FILES.filter((f) => f !== "pyodide-lock.json"), ...packageFiles(lock, packages)];
  let done = 0;
  onProgress(done, files.length);
  for (const file of files) {
    if (!(await cache.match(base + file))) {
      const response = await fetch(base + file);
      if (!response.ok) throw new Error(`Could not download ${file} (${response.status}).`);
      await cache.put(base + file, response);
    }
    onProgress(++done, files.length);
  }
  if (navigator.storage?.persist) void navigator.storage.persist();
}

function setupButton() {
  const section = document.getElementById("offline");
  const button = document.getElementById("btn-offline") as HTMLButtonElement | null;
  const status = document.getElementById("offline-status");
  if (!section || !button || !status) return;
  const base = section.dataset.pyodideBase ?? "";
  const packages = (section.dataset.packages ?? "").split(",").filter(Boolean);

  if (!("caches" in window) || !("serviceWorker" in navigator)) {
    section.hidden = true;
    return;
  }
  const ready = () => {
    status.textContent = "Ready. Python and the whole course will work without a connection.";
    button.textContent = "Downloaded";
    button.disabled = true;
  };
  void isDownloaded(base).then((ok) => ok && ready());

  button.addEventListener("click", async () => {
    button.disabled = true;
    try {
      await download(base, packages, (done, total) => {
        status.textContent = `Downloading Python… ${done} of ${total} files`;
      });
      ready();
    } catch (err) {
      status.textContent = `The download did not finish: ${(err as Error).message} Check your connection and try again.`;
      button.disabled = false;
    }
  });
}

setupButton();
