// Runs the browser runner (web/public/py/learn_runner.py via runner-core.js) on a real Pyodide
// in Node and checks it behaves like pytest does for every lesson in content/.
//
//   cd web && npm test
import { test, before } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { loadPyodide } from "pyodide";
import "../public/runner-core.js";

const here = path.dirname(fileURLToPath(import.meta.url));
const contentDir = path.resolve(here, "../../content");
const runnerSource = fs.readFileSync(path.resolve(here, "../public/py/learn_runner.py"), "utf8");

function listLessons() {
  const lessons = [];
  for (const mod of fs.readdirSync(contentDir).sort()) {
    const modDir = path.join(contentDir, mod);
    if (!fs.statSync(modDir).isDirectory()) continue;
    for (const lesson of fs.readdirSync(modDir).sort()) {
      const dir = path.join(modDir, lesson);
      if (!fs.statSync(dir).isDirectory()) continue;
      const read = (f) => fs.readFileSync(path.join(dir, f), "utf8");
      // local_only lessons need real pytest features/OS access and are not run in the browser.
      if (/^local_only:\s*true\s*$/m.test(read("lesson.md"))) continue;
      const packages = (read("lesson.md").match(/^packages:\s*\[(.*)\]\s*$/m)?.[1] ?? "")
        .split(",")
        .map((p) => p.trim().replace(/^["']|["']$/g, ""))
        .filter(Boolean);
      lessons.push({
        id: `${mod}/${lesson}`,
        packages,
        starter: read("starter.py"),
        solution: read("solution.py"),
        tests: read("test_exercise.py"),
      });
    }
  }
  return lessons;
}

let runner;
before(async () => {
  const pyodide = await loadPyodide();
  // Lessons in the optional data track declare the packages they need (numpy, pandas ...).
  const needed = [...new Set(lessons.flatMap((l) => l.packages))];
  if (needed.length > 0) await pyodide.loadPackage(needed);
  runner = globalThis.LearnRunner.create(pyodide, runnerSource);
});

const lessons = listLessons();

test("there are lessons to test", () => {
  assert.ok(lessons.length > 0);
});

for (const lesson of lessons) {
  test(`${lesson.id}: reference solution passes every check`, () => {
    const results = runner.runTests(lesson.solution, lesson.tests);
    assert.ok(results.length > 0, "no checks were found");
    const failing = results.filter((r) => !r.passed);
    assert.deepEqual(failing, [], "these checks failed: " + JSON.stringify(failing, null, 2));
  });

  test(`${lesson.id}: starter code fails at least one check, with a helpful message`, () => {
    const results = runner.runTests(lesson.starter, lesson.tests);
    const failing = results.filter((r) => !r.passed);
    assert.ok(failing.length > 0, "starter code should not pass already");
    for (const f of failing) assert.ok(f.message.length > 10, `check ${f.name} gave no useful message`);
  });
}

test("run_program captures print output", () => {
  const r = runner.runProgram('print("hi")\nprint(1 + 2)');
  assert.equal(r.output, "hi\n3\n");
  assert.equal(r.error, null);
});

test("run_program feeds input() from the Input box and echoes it", () => {
  const r = runner.runProgram('name = input("Name? ")\nprint("Hi", name)', "Sam");
  assert.equal(r.output, "Name? Sam\nHi Sam\n");
  assert.equal(r.error, null);
});

test("run_program explains missing input instead of hanging", () => {
  const r = runner.runProgram("input()");
  assert.match(r.error, /EOFError/);
  assert.match(r.error, /Input box/);
});

test("run_program reports runtime errors showing only the learner's code", () => {
  const r = runner.runProgram('x = 1\nprint(y)');
  assert.match(r.error, /line 2/);
  assert.match(r.error, /NameError: name 'y' is not defined/);
  assert.doesNotMatch(r.error, /learn_runner/);
});

test("run_program reports syntax errors", () => {
  const r = runner.runProgram('print("hello"');
  assert.match(r.error, /SyntaxError/);
  assert.match(r.error, /line 1/);
});

test("run_program keeps output printed before an error", () => {
  const r = runner.runProgram('print("before")\n1 / 0');
  assert.equal(r.output, "before\n");
  assert.match(r.error, /ZeroDivisionError/);
});

test("run_program stops runaway output", () => {
  const r = runner.runProgram('while True:\n    print("x" * 1000)');
  assert.match(r.error, /printed more than/);
});

test("run_program treats exit() as a normal end", () => {
  const r = runner.runProgram('print("a")\nraise SystemExit');
  assert.equal(r.output, "a\n");
  assert.equal(r.error, null);
});

test("programs do not leak state into the next run", () => {
  runner.runProgram("leaked = 123");
  const r = runner.runProgram("print('leaked' in globals())");
  assert.equal(r.output, "False\n");
});

test("runner: fixtures capsys and monkeypatch work and are undone afterwards", () => {
  const tests = [
    "def test_one(monkeypatch, capsys):",
    "    monkeypatch.setattr('builtins.input', lambda prompt='': '5')",
    "    import exercise",
    "    assert capsys.readouterr().out == '5\\n', 'wrong output'",
    "",
    "def test_two():",
    "    import builtins",
    "    assert builtins.input.__name__ == 'fake_input', 'input() was not restored'",
    "",
  ].join("\n");
  const results = runner.runTests("print(input())", tests);
  assert.deepEqual(results.map((r) => r.passed), [true, true], JSON.stringify(results));
});

test("runner: each check gets a fresh run of the learner's program", () => {
  const tests = [
    "def test_a(capsys):",
    "    import exercise",
    "    assert capsys.readouterr().out == 'ran\\n', 'a: program did not run'",
    "def test_b(capsys):",
    "    import exercise",
    "    assert capsys.readouterr().out == 'ran\\n', 'b: program did not run again'",
    "",
  ].join("\n");
  const results = runner.runTests("print('ran')", tests);
  assert.deepEqual(results.map((r) => r.passed), [true, true], JSON.stringify(results));
});

test("runner: learner errors are explained, assertion messages are passed through", () => {
  const tests = [
    "def test_runs():",
    "    import exercise",
    "def test_message():",
    "    assert False, 'custom hint for the learner'",
    "",
  ].join("\n");
  const [runs, message] = runner.runTests("print(undefined_name)", tests);
  assert.equal(runs.passed, false);
  assert.match(runs.message, /Your program stopped with an error/);
  assert.match(runs.message, /NameError/);
  assert.equal(message.message, "custom hint for the learner");
});

test("runner: syntax errors in the learner's code are explained", () => {
  const tests = "def test_runs():\n    import exercise\n";
  const [result] = runner.runTests("print(", tests);
  assert.equal(result.passed, false);
  assert.match(result.message, /syntax error/i);
});

test("runner: pytest.raises and pytest.approx are available", () => {
  const tests = [
    "import pytest",
    "def test_raises():",
    "    with pytest.raises(ZeroDivisionError):",
    "        1 / 0",
    "def test_approx():",
    "    assert 0.1 + 0.2 == pytest.approx(0.3), 'floats should be close'",
    "def test_not_raised():",
    "    with pytest.raises(ValueError):",
    "        pass",
    "",
  ].join("\n");
  const results = runner.runTests("", tests);
  assert.deepEqual(results.map((r) => r.passed), [true, true, false], JSON.stringify(results));
});

test("runner: unsupported fixtures give a clear message instead of crashing", () => {
  const [result] = runner.runTests("", "def test_tmp(request):\n    assert True, 'x'\n");
  assert.equal(result.passed, false);
  assert.match(result.message, /request/);
});

test("runner: tmp_path gives a fresh writable folder and monkeypatch.chdir moves into it and back", () => {
  const source = "from pathlib import Path\nPath('note.txt').write_text('hi')\nprint(Path('note.txt').read_text())\n";
  const tests = [
    "import os",
    "from pathlib import Path",
    "def test_a(tmp_path, monkeypatch, capsys):",
    "    before = os.getcwd()",
    "    monkeypatch.chdir(tmp_path)",
    "    import exercise",
    "    assert capsys.readouterr().out == 'hi\\n', 'program output'",
    "    assert (tmp_path / 'note.txt').read_text() == 'hi', 'file was written in the temp folder'",
    "    monkeypatch.undo()",
    "    assert os.getcwd() == before, 'chdir is undone'",
    "def test_b(tmp_path):",
    "    assert list(tmp_path.iterdir()) == [], 'each test gets an empty folder'",
    "    assert not Path('note.txt').exists(), 'nothing leaked into the working folder'",
  ].join("\n");
  const results = runner.runTests(source, tests);
  assert.deepEqual(results.map((r) => r.passed), [true, true], JSON.stringify(results));
});

test("runner: learner code is not affected by the runner's own __future__ imports (type hints stay real types)", () => {
  const source = "def f(x: int) -> str:\n    return str(x)\n";
  const tests = "def test_hints():\n    import exercise\n    assert exercise.f.__annotations__ == {'x': int, 'return': str}, 'hints should be real types'\n";
  const [result] = runner.runTests(source, tests);
  assert.equal(result.passed, true, JSON.stringify(result));
  const run = runner.runProgram("def f(x: int):\n    return x\nprint(f.__annotations__)\n", "");
  assert.match(run.output, /<class 'int'>/, JSON.stringify(run));
});

test("runner: an input() that no check provided raises a clear error", () => {
  const tests = "def test_needs_input():\n    import exercise\n";
  const [result] = runner.runTests("x = input('?')", tests);
  assert.equal(result.passed, false);
  assert.match(result.message, /Input box/);
});

test("runner: after the checks, stdout and input() are back to normal", () => {
  runner.runTests("print('x')", "def test_a():\n    import exercise\n");
  const r = runner.runProgram("print('still works')");
  assert.equal(r.output, "still works\n");
});
