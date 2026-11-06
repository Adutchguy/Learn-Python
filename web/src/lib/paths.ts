/** Build a URL that respects the site's base path (e.g. /Learn-Python/ on GitHub Pages). */
export function url(path = ""): string {
  const base = import.meta.env.BASE_URL.replace(/\/+$/, "");
  return `${base}/${path.replace(/^\/+/, "")}`;
}

export const REPO_URL = "https://github.com/Adutchguy/Learn-Python";
