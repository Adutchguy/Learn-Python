import { completedLessonIds, loadProgress, recordReview } from "./progress";
import { askForAnswer, pickedOption, questionEls, renderQuestion, revealAnswer, type Question } from "./question-ui";
import {
  DEFAULT_SESSION_SIZE,
  describeDay,
  dueQuestions,
  localDateString,
  nextDueDay,
  pickSession,
  type QueueState,
} from "./review-logic";

interface ReviewData {
  questions: (Question & { lesson: string })[];
  lessons: Record<string, { title: string; href: string }>;
  courseHref: string;
}

const data: ReviewData = JSON.parse(document.getElementById("review-data")!.textContent!);
const $ = <T extends HTMLElement>(id: string) => document.getElementById(id) as T;
const els = questionEls();

const intro = $("intro");
const quiz = $("quiz");
const result = $("result");
const status = $("review-status");
const beginBtn = $<HTMLButtonElement>("btn-begin");

let session: ReviewData["questions"] = [];
let index = 0;
let answered = false;
let correctCount = 0;
const missed: ReviewData["questions"] = [];

function state(): QueueState {
  return { completed: completedLessonIds(), entries: loadProgress().review, today: localDateString(new Date()) };
}

function plural(n: number, word: string): string {
  return `${n} ${word}${n === 1 ? "" : "s"}`;
}

function showIntro() {
  intro.hidden = false;
  quiz.hidden = true;
  result.hidden = true;

  const now = state();
  const due = dueQuestions(data.questions, now);
  const next = nextDueDay(data.questions, now);

  if (now.completed.size === 0) {
    status.textContent = "Your review queue starts filling when you finish a lesson. Come back after your first one.";
    beginBtn.hidden = true;
  } else if (due.length === 0) {
    status.textContent = next
      ? `You are all caught up. The next review is ${describeDay(next, now.today)}.`
      : "You are all caught up for now.";
    beginBtn.hidden = true;
  } else {
    const count = Math.min(due.length, DEFAULT_SESSION_SIZE);
    status.textContent = `${plural(due.length, "question")} due for review.`;
    beginBtn.textContent = `Start review (${plural(count, "question")})`;
    beginBtn.hidden = false;
  }
}

function startSession() {
  const now = state();
  session = pickSession(data.questions, now);
  if (session.length === 0) {
    showIntro();
    return;
  }
  index = 0;
  correctCount = 0;
  missed.length = 0;
  intro.hidden = true;
  result.hidden = true;
  quiz.hidden = false;
  showQuestion();
}

function showQuestion() {
  const q = session[index];
  answered = false;
  $("quiz-progress").textContent = `Question ${index + 1} of ${session.length}`;
  renderQuestion(els, q);
}

function finishQuestion(picked: number | null) {
  const q = session[index];
  answered = true;

  const lesson = data.lessons[q.lesson];
  let link: HTMLElement | undefined;
  if (lesson && picked !== q.answer) {
    const a = document.createElement("a");
    a.href = lesson.href;
    a.textContent = `Revisit “${lesson.title}”`;
    link = a;
  }
  const correct = revealAnswer(els, q, picked, link);
  recordReview(q.id, correct, state().today);
  if (correct) correctCount++;
  else missed.push(q);
  els.next.textContent = index === session.length - 1 ? "See my result" : "Next question";
}

function showResult() {
  quiz.hidden = true;
  result.hidden = false;

  $("result-title").textContent = `You got ${correctCount} of ${session.length} right.`;

  const missedBox = $("result-missed");
  missedBox.replaceChildren();
  if (missed.length > 0) {
    const heading = document.createElement("p");
    heading.textContent = "These will come back tomorrow. Worth a look:";
    const list = document.createElement("ul");
    const seen = new Set<string>();
    for (const q of missed) {
      const lesson = data.lessons[q.lesson];
      if (!lesson || seen.has(q.lesson)) continue;
      seen.add(q.lesson);
      const item = document.createElement("li");
      const a = document.createElement("a");
      a.href = lesson.href;
      a.textContent = lesson.title;
      item.append(a);
      list.append(item);
    }
    missedBox.append(heading, list);
  }

  const now = state();
  const remaining = dueQuestions(data.questions, now).length;
  const next = nextDueDay(data.questions, now);
  $("result-text").textContent =
    remaining > 0
      ? `${plural(remaining, "more question")} ${remaining === 1 ? "is" : "are"} due today.`
      : next
        ? `That is everything for now. The next review is ${describeDay(next, now.today)}.`
        : "That is everything for now.";

  const actions = $("result-actions");
  actions.replaceChildren();
  if (remaining > 0) {
    const more = document.createElement("button");
    more.type = "button";
    more.className = "button primary";
    more.textContent = "Keep going";
    more.addEventListener("click", startSession);
    actions.append(more);
  }
  const back = document.createElement("a");
  back.className = "button";
  back.href = data.courseHref;
  back.textContent = "Back to the course";
  actions.append(back);
}

beginBtn.addEventListener("click", startSession);

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
  if (index === session.length - 1) {
    showResult();
    return;
  }
  index++;
  showQuestion();
});

showIntro();
