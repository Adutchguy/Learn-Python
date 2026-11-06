import { defineConfig } from "astro/config";

// Served from https://adutchguy.github.io/Learn-Python/ (GitHub Pages project site).
export default defineConfig({
  site: "https://adutchguy.github.io",
  base: "/Learn-Python",
  trailingSlash: "always",
  markdown: {
    shikiConfig: {
      themes: { light: "github-light", dark: "github-dark" },
    },
  },
});
