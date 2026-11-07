import { completedLessonIds, exportProgress, importProgress, loadProgress, resetProgress } from "./progress";
import { dueQuestions, localDateString } from "./review-logic";

const lessonEls = Array.from(document.querySelectorAll<HTMLElement>("[data-lesson-id]"));
const summary = document.getElementById("progress-summary");
const startLink = document.getElementById("start-link") as HTMLAnchorElement | null;
const message = document.getElementById("progress-message");

const reviewLink = document.getElementById("review-link") as HTMLAnchorElement | null;
const reviewQuestions: { id: string; lesson: string }[] = JSON.parse(
  document.getElementById("review-index")?.textContent ?? "[]",
);

function refreshReview() {
  if (!reviewLink) return;
  const due = dueQuestions(reviewQuestions, {
    completed: completedLessonIds(),
    entries: loadProgress().review,
    today: localDateString(new Date()),
  }).length;
  reviewLink.hidden = due === 0;
  reviewLink.textContent = `Review: ${due} question${due === 1 ? "" : "s"} due`;
}

function refresh() {
  refreshReview();
  const progress = loadProgress();
  let done = 0;
  let skipped = 0;
  let trackDone = 0;
  let firstTodo: HTMLElement | undefined;
  for (const el of lessonEls) {
    const isTrack = el.dataset.optional === "true";
    const entry = progress.lessons[el.dataset.lessonId!];
    const isDone = entry?.done === true;
    const wasSkipped = isDone && entry?.placedOut === true;
    el.classList.toggle("done", isDone);
    el.querySelector<HTMLElement>(".check")!.textContent = wasSkipped ? "↷" : isDone ? "✔" : "";
    el.querySelector<HTMLElement>(".sr-status")!.textContent = wasSkipped
      ? " (skipped)"
      : isDone
        ? " (completed)"
        : "";
    if (isTrack) {
      if (isDone) trackDone++;
      continue; // optional lessons never count towards the core path or "Continue"
    }
    if (isDone) done++;
    if (wasSkipped) skipped++;
    else if (!firstTodo) firstTodo = el;
  }
  const coreTotal = lessonEls.filter((el) => el.dataset.optional !== "true").length;
  if (summary) {
    const extra = skipped > 0 ? ` (${skipped} skipped)` : "";
    const tracks = trackDone > 0 ? `, plus ${trackDone} optional track lesson${trackDone === 1 ? "" : "s"}` : "";
    summary.textContent = done === 0 && trackDone === 0 ? "" : `${done} of ${coreTotal} lessons complete${extra}${tracks}`;
  }
  if (startLink) {
    const next = firstTodo?.querySelector<HTMLAnchorElement>("a");
    if (done === 0 || !next) {
      if (done > 0 && !next) startLink.textContent = "Review lessons";
    } else {
      startLink.href = next.href;
      startLink.textContent = `Continue: ${next.textContent?.trim()}`;
    }
  }
}

function say(text: string, isError = false) {
  if (!message) return;
  message.textContent = text;
  message.className = isError ? "notice error" : "notice";
}

document.getElementById("btn-export")?.addEventListener("click", () => {
  const blob = new Blob([exportProgress()], { type: "application/json" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = "learn-python-progress.json";
  link.click();
  URL.revokeObjectURL(link.href);
  say("Progress file downloaded. Keep it somewhere safe.");
});

const fileInput = document.getElementById("file-import") as HTMLInputElement | null;
document.getElementById("btn-import")?.addEventListener("click", () => fileInput?.click());
fileInput?.addEventListener("change", async () => {
  const file = fileInput.files?.[0];
  fileInput.value = "";
  if (!file) return;
  const result = importProgress(await file.text());
  if (result.ok) {
    refresh();
    say(`Loaded progress for ${result.lessons} lesson${result.lessons === 1 ? "" : "s"}.`);
  } else {
    say(result.error, true);
  }
});

let resetArmed: ReturnType<typeof setTimeout> | undefined;
const resetBtn = document.getElementById("btn-reset-all") as HTMLButtonElement | null;
resetBtn?.addEventListener("click", () => {
  if (!resetArmed) {
    resetBtn.textContent = "Click again to erase all progress";
    resetArmed = setTimeout(() => {
      resetBtn.textContent = "Reset progress";
      resetArmed = undefined;
    }, 4000);
    return;
  }
  clearTimeout(resetArmed);
  resetArmed = undefined;
  resetBtn.textContent = "Reset progress";
  resetProgress();
  refresh();
  say("Progress erased on this device.");
});

refresh();
