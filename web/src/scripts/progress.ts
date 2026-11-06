// Learner progress lives only in this browser (localStorage). Nothing is sent anywhere.
// Storage can be unavailable (private mode, blocked cookies), so every access is guarded and
// we fall back to memory for the rest of the page's life.

const KEY = "learn-python:progress:v1";
const MAX_CODE_LENGTH = 50_000;

export interface LessonProgress {
  done: boolean;
  attempts: number; // failed checks so far
  hintsUsed: number;
  code?: string;
  completedAt?: string;
  /** Marked done by the placement test rather than by completing the lesson. */
  placedOut?: boolean;
}

interface Progress {
  version: 1;
  lessons: Record<string, LessonProgress>;
}

const blank = (): Progress => ({ version: 1, lessons: {} });
let memory: Progress | null = null;

function sanitize(raw: unknown): Progress | null {
  if (!raw || typeof raw !== "object") return null;
  const data = raw as { version?: unknown; lessons?: unknown };
  if (data.version !== 1 || !data.lessons || typeof data.lessons !== "object") return null;
  const clean = blank();
  for (const [id, value] of Object.entries(data.lessons as Record<string, unknown>)) {
    if (!value || typeof value !== "object") continue;
    const v = value as Record<string, unknown>;
    clean.lessons[id] = {
      done: v.done === true,
      attempts: Number.isFinite(v.attempts) ? Math.max(0, Math.floor(v.attempts as number)) : 0,
      hintsUsed: Number.isFinite(v.hintsUsed) ? Math.max(0, Math.min(3, Math.floor(v.hintsUsed as number))) : 0,
      code: typeof v.code === "string" ? v.code.slice(0, MAX_CODE_LENGTH) : undefined,
      completedAt: typeof v.completedAt === "string" ? v.completedAt.slice(0, 40) : undefined,
      placedOut: v.placedOut === true ? true : undefined,
    };
  }
  return clean;
}

export function loadProgress(): Progress {
  if (memory) return memory;
  try {
    const text = localStorage.getItem(KEY);
    if (text) {
      const parsed = sanitize(JSON.parse(text));
      if (parsed) return (memory = parsed);
    }
  } catch {
    /* storage unavailable or corrupt: start fresh */
  }
  return (memory = blank());
}

function persist(progress: Progress): void {
  memory = progress;
  try {
    localStorage.setItem(KEY, JSON.stringify(progress));
  } catch {
    /* keep working from memory */
  }
}

export function getLesson(id: string): LessonProgress {
  return loadProgress().lessons[id] ?? { done: false, attempts: 0, hintsUsed: 0 };
}

export function updateLesson(id: string, patch: Partial<LessonProgress>): LessonProgress {
  const progress = loadProgress();
  const next = { ...getLesson(id), ...patch };
  progress.lessons[id] = next;
  persist(progress);
  return next;
}

/** Mark lessons as skipped by the placement test. Lessons already done are left alone. Returns how many changed. */
export function markPlacedOut(ids: string[]): number {
  const progress = loadProgress();
  let changed = 0;
  for (const id of ids) {
    if (getLesson(id).done) continue;
    progress.lessons[id] = { ...getLesson(id), done: true, placedOut: true, completedAt: new Date().toISOString() };
    changed++;
  }
  persist(progress);
  return changed;
}

export function exportProgress(): string {
  return JSON.stringify(loadProgress(), null, 2);
}

/** Replace all progress with an exported file. Returns the number of lessons loaded. */
export function importProgress(text: string): { ok: true; lessons: number } | { ok: false; error: string } {
  let parsed: unknown;
  try {
    parsed = JSON.parse(text);
  } catch {
    return { ok: false, error: "That file is not valid JSON." };
  }
  const clean = sanitize(parsed);
  if (!clean) return { ok: false, error: "That does not look like a Learn-Python progress file." };
  persist(clean);
  return { ok: true, lessons: Object.keys(clean.lessons).length };
}

export function resetProgress(): void {
  persist(blank());
}
