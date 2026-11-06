import { markPlacedOut } from "./progress";
import { askForAnswer, pickedOption, questionEls, renderQuestion, revealAnswer, type Question } from "./question-ui";

interface LessonRef {
  id: string;
  title: string;
  href: string;
  skippable: boolean;
}
interface PlacementData {
  questions: Question[];
  lessons: LessonRef[];
  courseHref: string;
}

const MAX_MISSES = 2;
const data: PlacementData = JSON.parse(document.getElementById("placement-data")!.textContent!);
const $ = <T extends HTMLElement>(id: string) => document.getElementById(id) as T;

const intro = $("intro");
const quiz = $("quiz");
const result = $("result");
const els = questionEls();

let index = 0;
let misses = 0;
let firstMiss: Question | null = null;
let answered = false;

function showQuestion() {
  const q = data.questions[index];
  answered = false;
  $("quiz-progress").textContent = `Question ${index + 1} of up to ${data.questions.length}`;
  renderQuestion(els, q);
}

function finishQuestion(picked: number | null) {
  const q = data.questions[index];
  answered = true;
  const correct = revealAnswer(els, q, picked);
  if (!correct) {
    misses++;
    firstMiss ??= q;
  }
  const last = index === data.questions.length - 1;
  els.next.textContent = last || misses >= MAX_MISSES ? "See my result" : "Next question";
}

function lessonIndex(id: string | null): number {
  return id === null ? data.lessons.length : data.lessons.findIndex((l) => l.id === id);
}

function showResult() {
  quiz.hidden = true;
  result.hidden = false;

  const title = $("result-title");
  const text = $("result-text");
  const actions = $("result-actions");
  actions.replaceChildren();

  const startAt = firstMiss === null ? data.lessons.length : lessonIndex(firstMiss.lesson);
  const toSkip = data.lessons.slice(0, startAt).filter((l) => l.skippable);
  const target = data.lessons[startAt] as LessonRef | undefined;

  const link = (href: string, label: string, primary = false) => {
    const a = document.createElement("a");
    a.href = href;
    a.className = primary ? "button primary" : "button";
    a.textContent = label;
    return a;
  };
  const skipButton = (label: string) => {
    const b = document.createElement("button");
    b.type = "button";
    b.className = "button primary";
    b.textContent = label;
    b.addEventListener("click", () => {
      const changed = markPlacedOut(toSkip.map((l) => l.id));
      $("result-message").textContent =
        changed === 0
          ? "Those lessons were already marked as done."
          : `Marked ${changed} lesson${changed === 1 ? "" : "s"} as skipped. They show a ↷ on the course page.`;
      b.disabled = true;
    });
    return b;
  };

  if (firstMiss === null) {
    title.textContent = "You know everything covered so far.";
    text.textContent =
      "You answered every question correctly, including the ones that go beyond the lessons published so far. More lessons are on the way.";
    if (toSkip.length > 0) actions.append(skipButton(`Skip all ${toSkip.length} current lessons`));
    actions.append(link(data.courseHref, "Browse the course"));
    return;
  }

  if (!target) {
    // First miss was on a topic that has no lesson yet.
    title.textContent = "You are ahead of the current lessons.";
    text.textContent = `You know everything the published lessons cover. The next topic, ${firstMiss.topic?.toLowerCase() ?? "new material"}, is not written yet. Come back soon, or skip ahead and revisit anything later.`;
    if (toSkip.length > 0) actions.append(skipButton(`Skip all ${toSkip.length} current lessons`));
    actions.append(link(data.courseHref, "Browse the course"));
    return;
  }

  if (startAt === 0 || toSkip.length === 0) {
    title.textContent = "Start with the first lesson.";
    text.textContent =
      "The basics are a great place to begin, and the lessons are short. Nothing to skip: you will get comfortable quickly.";
    actions.append(link(data.lessons[0].href, `Start: ${data.lessons[0].title}`, true));
    return;
  }

  title.textContent = `Start with “${target.title}”.`;
  text.textContent = `You are comfortable with the earlier material. You can skip the ${toSkip.length} earlier lesson${toSkip.length === 1 ? "" : "s"} (they are marked as done, and you can still open any of them) or work through them all. Skipping does not delete anything.`;
  actions.append(skipButton(`Skip ahead (${toSkip.length} lessons)`));
  actions.append(link(target.href, `Go to “${target.title}”`));
  actions.append(link(data.lessons[0].href, "Start from lesson 1"));
}

$("btn-begin").addEventListener("click", () => {
  intro.hidden = true;
  quiz.hidden = false;
  showQuestion();
});

els.form.addEventListener("submit", (event) => {
  event.preventDefault();
  if (answered) return;
  const choice = pickedOption(els);
  if (choice === null) {
    askForAnswer(els);
    return;
  }
  finishQuestion(choice);
});

els.unsure.addEventListener("click", () => {
  if (!answered) finishQuestion(null);
});

els.next.addEventListener("click", () => {
  if (misses >= MAX_MISSES || index === data.questions.length - 1) {
    showResult();
    return;
  }
  index++;
  showQuestion();
});
