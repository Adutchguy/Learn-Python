import { loadProgress, markPlacedOut } from "./progress";

interface FastTrackData {
  skip: string[];
  lessons: Record<string, { title: string; href: string }>;
  order: string[];
  courseHref: string;
}

const data: FastTrackData = JSON.parse(document.getElementById("fast-track-data")?.textContent ?? "{}");
const button = document.getElementById("btn-use-route") as HTMLButtonElement | null;
const message = document.getElementById("route-message");

/** The first lesson in course order that is not yet done (completed or skipped). */
function firstTodo(): string | undefined {
  const lessons = loadProgress().lessons;
  return data.order.find((id) => lessons[id]?.done !== true);
}

button?.addEventListener("click", () => {
  const changed = markPlacedOut(data.skip);
  if (!message) return;
  message.replaceChildren();
  message.append(
    changed === 0
      ? "Nothing to change: those lessons are already marked as done. "
      : `Marked ${changed} lesson${changed === 1 ? "" : "s"} as skipped. `,
  );
  const next = firstTodo();
  const target = next ? data.lessons[next] : undefined;
  if (target) {
    const link = document.createElement("a");
    link.href = target.href;
    link.textContent = `Start with: ${target.title}`;
    message.append(link);
  } else {
    const link = document.createElement("a");
    link.href = data.courseHref;
    link.textContent = "Back to the course";
    message.append(link);
  }
});
