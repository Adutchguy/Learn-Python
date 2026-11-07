import { defineConfig } from "astro/config";
import pwa from "./integrations/pwa.mjs";

// Served from https://adutchguy.github.io/Learn-Python/ (GitHub Pages project site).
export default defineConfig({
  site: "https://adutchguy.github.io",
  base: "/Learn-Python",
  trailingSlash: "always",
  integrations: [pwa()],
  markdown: {
    shikiConfig: {
      themes: { light: "github-light-high-contrast", dark: "github-dark-high-contrast" },
    },
  },
});
