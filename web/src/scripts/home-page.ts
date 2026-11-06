import { exportProgress, importProgress, loadProgress, resetProgress } from "./progress";

const lessonEls = Array.from(document.querySelectorAll<HTMLElement>("[data-lesson-id]"));
const summary = document.getElementById("progress-summary");
const startLink = document.getElementById("start-link") as HTMLAnchorElement | null;
const message = document.getElementById("progress-message");

function refresh() {
  const progress = loadProgress();
  let done = 0;
  let firstTodo: HTMLElement | undefined;
  for (const el of lessonEls) {
    const isDone = progress.lessons[el.dataset.lessonId!]?.done === true;
    el.classList.toggle("done", isDone);
    el.querySelector<HTMLElement>(".check")!.textContent = isDone ? "✔" : "";
    el.querySelector<HTMLElement>(".sr-status")!.textContent = isDone ? " (completed)" : "";
    if (isDone) done++;
    else if (!firstTodo) firstTodo = el;
  }
  if (summary) {
    summary.textContent = done === 0 ? "" : `${done} of ${lessonEls.length} lessons complete`;
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
