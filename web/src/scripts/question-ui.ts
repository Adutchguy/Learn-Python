// Shared by the placement test and the review queue: shows one multiple-choice question and
// reveals the answer. Both pages use the same markup (see placement.astro and review.astro).

export interface Question {
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

export interface QuestionEls {
  form: HTMLFormElement;
  prompt: HTMLElement;
  code: HTMLElement;
  stdin: HTMLElement;
  options: HTMLElement;
  feedback: HTMLElement;
  check: HTMLButtonElement;
  unsure: HTMLButtonElement;
  next: HTMLButtonElement;
}

export function questionEls(): QuestionEls {
  const get = <T extends HTMLElement>(id: string) => document.getElementById(id) as T;
  return {
    form: get("question-form"),
    prompt: get("q-prompt"),
    code: get("q-code"),
    stdin: get("q-stdin"),
    options: get("q-options"),
    feedback: get("q-feedback"),
    check: get("btn-check"),
    unsure: get("btn-unsure"),
    next: get("btn-next"),
  };
}

export function renderQuestion(els: QuestionEls, q: Question): void {
  els.prompt.textContent = q.prompt;
  els.code.hidden = !q.code;
  els.code.querySelector("code")!.textContent = q.code ?? "";

  els.stdin.hidden = q.stdin === undefined;
  if (q.stdin !== undefined) {
    els.stdin.textContent = `The user types: ${q.stdin.replace(/\n$/, "").replace(/\n/g, ", then ")}`;
  }

  els.options.replaceChildren();
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
    els.options.append(label);
  });

  els.feedback.hidden = true;
  els.feedback.className = "banner";
  els.next.hidden = true;
  els.check.disabled = false;
  els.unsure.disabled = false;
  els.options.querySelector<HTMLInputElement>("input")?.focus();
}

/** The option the learner picked, or null if none is selected. */
export function pickedOption(els: QuestionEls): number | null {
  const picked = els.form.querySelector<HTMLInputElement>("input[name=answer]:checked");
  return picked ? Number(picked.value) : null;
}

export function askForAnswer(els: QuestionEls): void {
  els.feedback.textContent = "Pick an answer, or choose “I'm not sure”.";
  els.feedback.className = "banner try-again";
  els.feedback.hidden = false;
}

/** Lock the options, highlight the right one and show the explanation. Returns whether it was correct. */
export function revealAnswer(els: QuestionEls, q: Question, picked: number | null, extra?: HTMLElement): boolean {
  const correct = picked === q.answer;
  els.check.disabled = true;
  els.unsure.disabled = true;
  els.options.querySelectorAll("input").forEach((el) => (el.disabled = true));
  els.options.querySelectorAll<HTMLElement>(".q-option").forEach((label, i) => {
    label.classList.toggle("is-answer", i === q.answer);
    label.classList.toggle("is-wrong", picked === i && !correct);
  });

  const lead = correct ? "Correct. " : picked === null ? "No problem. " : "Not quite. ";
  const answerLine = correct
    ? ""
    : `The answer is ${q.options[q.answer].includes("\n") ? "the highlighted option" : `“${q.options[q.answer]}”`}. `;
  els.feedback.textContent = `${lead}${answerLine}${q.explanation}`;
  if (extra) els.feedback.append(" ", extra);
  els.feedback.className = correct ? "banner success" : "banner try-again";
  els.feedback.hidden = false;
  els.next.hidden = false;
  els.next.focus();
  return correct;
}
