import { defineCollection } from "astro:content";
import { glob } from "astro/loaders";
import { z } from "astro/zod";

// Lessons live in the repository-level `content/` folder, which also feeds the local track.
// The schema mirrors tools/content.py, which is the stricter validator run in CI.
const lessons = defineCollection({
  loader: glob({
    base: "../content",
    pattern: "**/lesson.md",
    generateId: ({ entry }) => entry.replace(/\/lesson\.md$/, ""),
  }),
  schema: z.object({
    title: z.string(),
    minutes: z.number().int().min(1).max(60),
    prereqs: z.array(z.string()),
    concepts: z.array(z.string()).min(1),
    local_only: z.boolean(),
    hints: z.array(z.string()).length(3),
    packages: z.array(z.string()).default([]),
    broken_starter: z.boolean().optional(),
  }),
});

export const collections = { lessons };
