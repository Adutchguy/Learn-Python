import { EditorView, basicSetup } from "codemirror";
import { keymap } from "@codemirror/view";
import { indentWithTab } from "@codemirror/commands";
import { python } from "@codemirror/lang-python";
import { oneDark } from "@codemirror/theme-one-dark";
import { PythonClient, StoppedError, type TestResult } from "./python-client";
import { getLesson, updateLesson } from "./progress";

interface LessonData {
  id: string;
  starter: string;
  solution: string;
  tests: string;
  hints: string[];
  localOnly: boolean;
  nextHref: string | null;
  python: { workerUrl: string; indexURL: string; runnerUrl: string };
}

const SOLUTION_UNLOCK_AFTER = 3; // failed checks

const $ = <T extends HTMLElement>(id: string) => document.getElementById(id) as T;
const data: LessonData = JSON.parse($("lesson-data").textContent || "{}");

if (!data.localOnly) init();

function init() {
  const progress = getLesson(data.id);
  const client = new PythonClient(data.python);

  const runBtn = $<HTMLButtonElement>("btn-run");
  const checkBtn = $<HTMLButtonElement>("btn-check");
  const stopBtn = $<HTMLButtonElement>("btn-stop");
  const resetBtn = $<HTMLButtonElement>("btn-reset");
  const hintBtn = $<HTMLButtonElement>("btn-hint");
  const solutionBtn = $<HTMLButtonElement>("btn-solution");
  const status = $("status");
  const output = $("output");
  const results = $("results");
  const banner = $("banner");
  const stdin = $<HTMLTextAreaElement>("stdin");
  const hintList = $("hint-list");
  const solutionBox = $("solution-box");

  // ---------------------------------------------------------------- editor
  const dark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  let saveTimer: ReturnType<typeof setTimeout> | undefined;
  const view = new EditorView({
    parent: $("editor"),
    doc: progress.code ?? data.starter,
    extensions: [
      basicSetup,
      python(),
      keymap.of([
        { key: "Mod-Enter", run: () => (void runCode(), true) },
        indentWithTab,
      ]),
      dark ? oneDark : [],
      EditorView.contentAttributes.of({ "aria-label": "Python code editor. Press Escape then Tab to leave the editor." }),
      EditorView.updateListener.of((update) => {
        if (!update.docChanged) return;
        clearTimeout(saveTimer);
        saveTimer = setTimeout(() => updateLesson(data.id, { code: view.state.doc.toString() }), 400);
      }),
    ],
  });
  const code = () => view.state.doc.toString();

  // ---------------------------------------------------------------- python
  let busy = false;
  const setBusy = (value: boolean) => {
    busy = value;
    runBtn.disabled = checkBtn.disabled = value;
    stopBtn.hidden = !value;
  };

  client.onStatus = (state, detail) => {
    status.dataset.state = state;
    status.textContent =
      state === "loading"
        ? "Loading Python… the first time takes a few seconds."
        : state === "ready"
          ? "Python is ready."
          : state === "busy"
            ? "Running…"
            : `Python could not start. ${detail ?? ""}`;
  };
  client.start();

  const showError = (error: unknown) => {
    const text = error instanceof Error ? error.message : String(error);
    output.className = "output has-error";
    output.textContent = text;
    if (!(error instanceof StoppedError)) results.replaceChildren();
  };

  async function runCode() {
    if (busy) return;
    setBusy(true);
    banner.hidden = true;
    results.replaceChildren();
    try {
      const result = await client.run(code(), stdin.value);
      output.className = result.error ? "output has-error" : "output";
      output.textContent = result.output + (result.error ? (result.output && !result.output.endsWith("\n") ? "\n" : "") + result.error : "");
      if (!result.output && !result.error) output.textContent = "(Your program ran and printed nothing.)";
    } catch (error) {
      showError(error);
    } finally {
      setBusy(false);
    }
  }

  async function checkCode() {
    if (busy) return;
    setBusy(true);
    banner.hidden = true;
    output.textContent = "";
    try {
      const outcome = await client.test(code(), data.tests);
      renderResults(outcome);
      const allPassed = outcome.length > 0 && outcome.every((r) => r.passed);
      if (allPassed) {
        updateLesson(data.id, { done: true, completedAt: new Date().toISOString(), code: code() });
        showBanner(true);
      } else {
        const attempts = getLesson(data.id).attempts + 1;
        updateLesson(data.id, { attempts, code: code() });
        showBanner(false);
      }
      refreshSolutionButton();
    } catch (error) {
      showError(error);
    } finally {
      setBusy(false);
    }
  }

  // --------------------------------------------------------------- results
  const prettyName = (name: string) => name.replace(/^test_/, "").replace(/_/g, " ");

  function renderResults(outcome: TestResult[]) {
    const items = outcome.map((r) => {
      const li = document.createElement("li");
      li.className = r.passed ? "pass" : "fail";
      const label = document.createElement("span");
      label.textContent = `${r.passed ? "✔ Passed" : "✘ Not yet"}: ${prettyName(r.name)}`;
      li.append(label);
      if (!r.passed && r.message) {
        const pre = document.createElement("pre");
        pre.textContent = r.message;
        li.append(pre);
      }
      return li;
    });
    results.replaceChildren(...items);
  }

  function showBanner(success: boolean) {
    banner.hidden = false;
    banner.className = success ? "banner success" : "banner try-again";
    banner.replaceChildren();
    const heading = document.createElement("strong");
    heading.textContent = success ? "Nice work! Every check passed." : "Not quite yet. Read the messages below and try again.";
    banner.append(heading);
    if (success && data.nextHref) {
      const link = document.createElement("a");
      link.className = "button primary";
      link.href = data.nextHref;
      link.textContent = "Next lesson →";
      banner.append(" ", link);
    }
    banner.scrollIntoView({ block: "nearest", behavior: "smooth" });
  }

  // ------------------------------------------------------------- hints etc.
  let hintsShown = 0;
  function showHints(count: number) {
    hintList.replaceChildren(
      ...data.hints.slice(0, count).map((hint, i) => {
        const li = document.createElement("li");
        li.textContent = `Hint ${i + 1}: ${hint}`;
        return li;
      }),
    );
    hintsShown = count;
    hintBtn.textContent = count >= data.hints.length ? "No more hints" : `Show hint ${count + 1} of ${data.hints.length}`;
    hintBtn.disabled = count >= data.hints.length;
  }
  showHints(Math.min(progress.hintsUsed, data.hints.length));
  hintBtn.addEventListener("click", () => {
    showHints(hintsShown + 1);
    updateLesson(data.id, { hintsUsed: hintsShown });
  });

  function refreshSolutionButton() {
    const current = getLesson(data.id);
    const remaining = SOLUTION_UNLOCK_AFTER - current.attempts;
    const unlocked = current.done || remaining <= 0;
    solutionBtn.disabled = !unlocked || !solutionBox.hidden;
    solutionBtn.textContent = unlocked
      ? solutionBox.hidden
        ? "Show the solution"
        : "Solution shown"
      : `Solution unlocks after ${remaining} more unsuccessful check${remaining === 1 ? "" : "s"}`;
  }
  refreshSolutionButton();
  solutionBtn.addEventListener("click", () => {
    const pre = document.createElement("pre");
    pre.className = "solution";
    pre.textContent = data.solution;
    solutionBox.replaceChildren(pre);
    solutionBox.hidden = false;
    refreshSolutionButton();
  });

  // ---------------------------------------------------------------- buttons
  runBtn.addEventListener("click", runCode);
  checkBtn.addEventListener("click", checkCode);
  stopBtn.addEventListener("click", () => {
    client.stop("Stopped.");
    setBusy(false);
  });

  let resetArmed: ReturnType<typeof setTimeout> | undefined;
  resetBtn.addEventListener("click", () => {
    if (!resetArmed) {
      resetBtn.textContent = "Click again to reset";
      resetArmed = setTimeout(() => {
        resetBtn.textContent = "Reset code";
        resetArmed = undefined;
      }, 3000);
      return;
    }
    clearTimeout(resetArmed);
    resetArmed = undefined;
    resetBtn.textContent = "Reset code";
    view.dispatch({ changes: { from: 0, to: view.state.doc.length, insert: data.starter } });
    updateLesson(data.id, { code: data.starter });
    output.textContent = "";
    results.replaceChildren();
    banner.hidden = true;
  });
}
