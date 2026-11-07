/*
 * Service worker: lets the course work offline.
 *
 * - The site itself (pages, scripts, styles, the Python runner) is listed in PRECACHE, which the
 *   build fills in (see integrations/pwa.mjs). It is stored when the worker installs.
 * - Python itself (Pyodide) comes from a CDN. It is cached the first time it is used, or all at
 *   once when the learner presses "Download for offline" on the home page.
 *
 * VERSION (filled in by the build) changes whenever any site file changes, which gives each release its own cache.
 */
const VERSION = "__VERSION__";
const SHELL_CACHE = "lp-shell-" + VERSION;
const PYODIDE_CACHE = "lp-pyodide"; // kept across releases: the URLs already contain Pyodide's version
const PRECACHE = __PRECACHE__;
const NOT_FOUND_PAGE = "__NOT_FOUND__";

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches
      .open(SHELL_CACHE)
      .then((cache) => cache.addAll(PRECACHE))
      .then(() => self.skipWaiting()),
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((keys) =>
        Promise.all(keys.filter((k) => k.startsWith("lp-shell-") && k !== SHELL_CACHE).map((k) => caches.delete(k))),
      )
      .then(() => self.clients.claim()),
  );
});

function isPyodide(url) {
  return url.hostname === "cdn.jsdelivr.net" && url.pathname.startsWith("/pyodide/");
}

self.addEventListener("fetch", (event) => {
  const request = event.request;
  if (request.method !== "GET") return;
  const url = new URL(request.url);

  if (isPyodide(url)) {
    event.respondWith(cacheFirst(request, PYODIDE_CACHE));
    return;
  }
  if (url.origin !== self.location.origin) return;

  if (request.mode === "navigate") {
    event.respondWith(networkFirstPage(request));
  } else {
    // Built assets have hashed names and the rest rarely changes: answer from the cache, fall back to the network.
    event.respondWith(cacheFirst(request, SHELL_CACHE));
  }
});

async function cacheFirst(request, cacheName) {
  const cache = await caches.open(cacheName);
  const hit = await cache.match(request, { ignoreSearch: cacheName === SHELL_CACHE, ignoreVary: true });
  if (hit) return hit;
  const response = await fetch(request);
  if (response.ok) cache.put(request, response.clone());
  return response;
}

async function networkFirstPage(request) {
  const cache = await caches.open(SHELL_CACHE);
  try {
    const response = await fetch(request);
    if (response.ok) cache.put(request, response.clone());
    return response;
  } catch (err) {
    const hit = await cache.match(request, { ignoreSearch: true, ignoreVary: true });
    if (hit) return hit;
    const fallback = await cache.match(NOT_FOUND_PAGE);
    if (fallback) return fallback;
    throw err;
  }
}
