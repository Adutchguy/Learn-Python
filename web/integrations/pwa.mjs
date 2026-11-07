// Astro integration: after the site is built, fill in the service worker's file list and version.
import { createHash } from "node:crypto";
import { readdir, readFile, writeFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import path from "node:path";

const SKIP_DIRS = new Set(["_pyodide_test"]); // test fixtures that the end-to-end test copies into dist
const SKIP_FILES = new Set(["sw.js"]);

async function walk(dir, prefix = "") {
  const out = [];
  for (const entry of await readdir(dir, { withFileTypes: true })) {
    if (entry.isDirectory()) {
      if (SKIP_DIRS.has(entry.name)) continue;
      out.push(...(await walk(path.join(dir, entry.name), `${prefix}${entry.name}/`)));
    } else if (!SKIP_FILES.has(entry.name) && !entry.name.endsWith(".map")) {
      out.push(`${prefix}${entry.name}`);
    }
  }
  return out.sort();
}

export default function pwa() {
  let base = "/";
  return {
    name: "learn-python-pwa",
    hooks: {
      "astro:config:done": ({ config }) => {
        base = config.base.endsWith("/") ? config.base : `${config.base}/`;
      },
      "astro:build:done": async ({ dir }) => {
        const root = fileURLToPath(dir);
        const files = await walk(root);
        const hash = createHash("sha256");
        const urls = [];
        for (const file of files) {
          hash.update(file);
          hash.update(await readFile(path.join(root, file)));
          if (file === "index.html") urls.push(base);
          else if (file.endsWith("/index.html")) urls.push(`${base}${file.slice(0, -"index.html".length)}`);
          else urls.push(`${base}${file}`);
        }
        const swPath = path.join(root, "sw.js");
        const template = await readFile(swPath, "utf8");
        const sw = template
          .replace("__VERSION__", hash.digest("hex").slice(0, 12))
          .replace("__PRECACHE__", JSON.stringify([...new Set(urls)], null, 1))
          .replace("__NOT_FOUND__", `${base}404.html`);
        await writeFile(swPath, sw);
        console.log(`[pwa] service worker lists ${urls.length} files for offline use`);
      },
    },
  };
}
