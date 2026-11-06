import fs from "node:fs";
import path from "node:path";
import { getCollection, type CollectionEntry } from "astro:content";
import { url } from "./paths";

// The build runs from the web/ folder (npm run build), so content/ is one level up.
const CONTENT_DIR = path.resolve(process.cwd(), "../content");

export interface LessonInfo {
  id: string;
  moduleSlug: string;
  lessonSlug: string;
  title: string;
  minutes: number;
  concepts: string[];
  localOnly: boolean;
  hints: string[];
  href: string;
  entry: CollectionEntry<"lessons">;
}

export interface ModuleInfo {
  slug: string;
  number: number;
  title: string;
  description: string;
  lessons: LessonInfo[];
}

export async function loadCourse(): Promise<ModuleInfo[]> {
  const entries = (await getCollection("lessons")).sort((a, b) => a.id.localeCompare(b.id));
  const modules = new Map<string, ModuleInfo>();

  for (const entry of entries) {
    const [moduleSlug, lessonSlug] = entry.id.split("/");
    let mod = modules.get(moduleSlug);
    if (!mod) {
      const meta = JSON.parse(fs.readFileSync(path.join(CONTENT_DIR, moduleSlug, "module.json"), "utf8"));
      mod = {
        slug: moduleSlug,
        number: parseInt(moduleSlug.split("-")[0], 10),
        title: meta.title,
        description: meta.description,
        lessons: [],
      };
      modules.set(moduleSlug, mod);
    }
    mod.lessons.push({
      id: entry.id,
      moduleSlug,
      lessonSlug,
      title: entry.data.title,
      minutes: entry.data.minutes,
      concepts: entry.data.concepts,
      localOnly: entry.data.local_only,
      hints: entry.data.hints,
      href: url(`lessons/${moduleSlug}/${lessonSlug}/`),
      entry,
    });
  }
  return [...modules.values()];
}

export function flattenLessons(modules: ModuleInfo[]): LessonInfo[] {
  return modules.flatMap((m) => m.lessons);
}

export interface Exercise {
  starter: string;
  solution: string;
  tests: string;
}

export function readExercise(lessonId: string): Exercise {
  const dir = path.join(CONTENT_DIR, ...lessonId.split("/"));
  const read = (name: string) => fs.readFileSync(path.join(dir, name), "utf8").replace(/\r\n/g, "\n");
  return { starter: read("starter.py"), solution: read("solution.py"), tests: read("test_exercise.py") };
}

/** The Pyodide version is whatever the Node tests ran against (pinned in package.json). */
export function pyodideVersion(): string {
  const pkg = JSON.parse(fs.readFileSync(path.resolve(process.cwd(), "node_modules/pyodide/package.json"), "utf8"));
  return pkg.version as string;
}

export interface PlacementQuestion {
  id: string;
  lesson: string | null;
  topic?: string;
  kind?: "output" | "error";
  prompt: string;
  code?: string;
  stdin?: string;
  options: string[];
  answer: number;
  explanation: string;
}

export function loadPlacementQuestions(): PlacementQuestion[] {
  const file = path.join(CONTENT_DIR, "placement", "questions.json");
  return JSON.parse(fs.readFileSync(file, "utf8")).questions as PlacementQuestion[];
}
