// Spaced-review scheduling. Pure functions only (no DOM, no storage) so they can be tested in Node.
//
// A simple Leitner system. Each question has a "box" from 0 to 5:
//   box 0  answered wrong last time        -> ask again tomorrow
//   box 1  answered right once             -> ask again tomorrow
//   box 2..5 answered right again and again -> 3, 7, 14, then 30 days
// A correct answer moves a question up one box; a wrong (or "not sure") answer drops it to box 0.
// Dates are local calendar days written YYYY-MM-DD, so "tomorrow" means tomorrow where the learner is.

export interface ReviewEntry {
  box: number;
  due: string;
  seen: number;
}

export const MAX_BOX = 5;
export const INTERVAL_DAYS = [1, 1, 3, 7, 14, 30];
export const DEFAULT_SESSION_SIZE = 10;
export const DATE_PATTERN = /^\d{4}-\d{2}-\d{2}$/;

export function localDateString(date: Date): string {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, "0");
  const d = String(date.getDate()).padStart(2, "0");
  return `${y}-${m}-${d}`;
}

export function addDays(day: string, days: number): string {
  const [y, m, d] = day.split("-").map(Number);
  return localDateString(new Date(y, m - 1, d + days)); // Date handles month and year roll-over
}

export function nextEntry(previous: ReviewEntry | undefined, correct: boolean, today: string): ReviewEntry {
  const box = correct ? Math.min(MAX_BOX, (previous?.box ?? 0) + 1) : 0;
  return { box, due: addDays(today, INTERVAL_DAYS[box]), seen: (previous?.seen ?? 0) + 1 };
}

export interface ReviewQuestionRef {
  id: string;
  lesson: string;
}

export interface QueueState {
  /** Lessons the learner has really completed (not skipped by the placement test). */
  completed: ReadonlySet<string>;
  entries: Readonly<Record<string, ReviewEntry>>;
  today: string;
}

function eligible<T extends ReviewQuestionRef>(questions: readonly T[], state: QueueState): T[] {
  return questions.filter((q) => state.completed.has(q.lesson));
}

function isDue(entry: ReviewEntry | undefined, today: string): boolean {
  return entry === undefined || entry.due <= today;
}

/** All due questions: overdue ones first (oldest first), then new ones in course order. */
export function dueQuestions<T extends ReviewQuestionRef>(questions: readonly T[], state: QueueState): T[] {
  const due = eligible(questions, state).filter((q) => isDue(state.entries[q.id], state.today));
  const dueDate = (q: T) => state.entries[q.id]?.due;
  const seen = due.filter((q) => dueDate(q) !== undefined).sort((a, b) => dueDate(a)!.localeCompare(dueDate(b)!));
  const fresh = due.filter((q) => dueDate(q) === undefined);
  return [...seen, ...fresh];
}

export function pickSession<T extends ReviewQuestionRef>(
  questions: readonly T[],
  state: QueueState,
  limit = DEFAULT_SESSION_SIZE,
): T[] {
  return dueQuestions(questions, state).slice(0, limit);
}

/** The earliest future day something becomes due, or null if nothing is scheduled. */
export function nextDueDay<T extends ReviewQuestionRef>(questions: readonly T[], state: QueueState): string | null {
  const days = eligible(questions, state)
    .map((q) => state.entries[q.id]?.due)
    .filter((due): due is string => due !== undefined && due > state.today)
    .sort();
  return days[0] ?? null;
}

export function describeDay(day: string, today: string): string {
  if (day === addDays(today, 1)) return "tomorrow";
  const [y, m, d] = day.split("-").map(Number);
  const label = new Date(y, m - 1, d).toLocaleDateString(undefined, { weekday: "long", month: "short", day: "numeric" });
  return `on ${label}`;
}
