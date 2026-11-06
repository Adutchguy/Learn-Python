import { markPlacedOut } from "./progress";

interface Question {
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
const form = $<HTMLFormElement>("question-form");
const optionsEl = $("q-options");
const feedback = $("q-feedback");
const nextBtn = $<HTMLButtonElement>("btn-next");
const checkBtn = $<HTMLButtonElement>("btn-check");
const unsureBtn = $<HTMLButtonElement>("btn-unsure");

let index = 0;
let misses = 0;
let firstMiss: Question | null = null;
let answered = false;

function showQuestion() {
  const q = data.questions[index];
  answered = false;
  $("quiz-progress").textContent = `Question ${index + 1} of up to ${data.questions.length}`;
  $("q-prompt").textContent = q.prompt;

  const codeBlock = $("q-code");
  codeBlock.hidden = !q.code;
  codeBlock.querySelector("code")!.textContent = q.code ?? "";

  const stdin = $("q-stdin");
  stdin.hidden = q.stdin === undefined;
  if (q.stdin !== undefined) stdin.textContent = `The user types: ${q.stdin.replace(/\n$/, "").replace(/\n/g, ", then ")}`;

  optionsEl.replaceChildren();
  q.options.forEach((text, i) => {
    const label = document.createElement("label");
    label.className = "q-option";
    const input = document.createElement("input");
    input.type = "radio";
    input.name = "answer";
    input.value = String(i);
    const body = document.createElement("span");
    body.className = "q-option-text";
    body.textContent = text;
    label.append(input, body);
    optionsEl.append(label);
  });

  feedback.hidden = true;
  feedback.className = "banner";
  nextBtn.hidden = true;
  checkBtn.disabled = false;
  unsureBtn.disabled = false;
  optionsEl.querySelector<HTMLInputElement>("input")?.focus();
}

function finishQuestion(correct: boolean, picked: number | null) {
  const q = data.questions[index];
  answered = true;
  checkBtn.disabled = true;
  unsureBtn.disabled = true;
  optionsEl.querySelectorAll("input").forEach((el) => (el.disabled = true));

  optionsEl.querySelectorAll<HTMLElement>(".q-option").forEach((label, i) => {
    label.classList.toggle("is-answer", i === q.answer);
    label.classList.toggle("is-wrong", picked === i && !correct);
  });

  if (!correct) {
    misses++;
    firstMiss ??= q;
  }
  const lead = correct ? "Correct. " : picked === null ? "No problem. " : "Not quite. ";
  const answerLine = correct ? "" : `The answer is ${q.options[q.answer].includes("\n") ? "the highlighted option" : `“${q.options[q.answer]}”`}. `;
  feedback.textContent = `${lead}${answerLine}${q.explanation}`;
  feedback.className = correct ? "banner success" : "banner try-again";
  feedback.hidden = false;

  const last = index === data.questions.length - 1;
  const stop = misses >= MAX_MISSES;
  nextBtn.textContent = last || stop ? "See my result" : "Next question";
  nextBtn.hidden = false;
  nextBtn.focus();
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
      "You answered every question correctly, including the ones that go beyond the lessons published so far. More lessons on lists, dictionaries and functions are on the way.";
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

form.addEventListener("submit", (event) => {
  event.preventDefault();
  if (answered) return;
  const picked = form.querySelector<HTMLInputElement>("input[name=answer]:checked");
  if (!picked) {
    feedback.textContent = "Pick an answer, or choose “I'm not sure”.";
    feedback.className = "banner try-again";
    feedback.hidden = false;
    return;
  }
  const choice = Number(picked.value);
  finishQuestion(choice === data.questions[index].answer, choice);
});

unsureBtn.addEventListener("click", () => {
  if (!answered) finishQuestion(false, null);
});

nextBtn.addEventListener("click", () => {
  if (misses >= MAX_MISSES || index === data.questions.length - 1) {
    showResult();
    return;
  }
  index++;
  showQuestion();
});
