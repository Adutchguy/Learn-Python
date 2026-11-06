/*
 * Glue between JavaScript and web/public/py/learn_runner.py.
 *
 * It has no import/export on purpose: it only sets `LearnRunner` on the global object, so the
 * browser worker and the Node tests can both simply `import "./runner-core.js"` and exercise the
 * exact same code path.
 */
(function (root) {
  "use strict";

  /** Create a runner on an already-loaded Pyodide instance. */
  function create(pyodide, runnerSource) {
    pyodide.FS.mkdirTree("/home/pyodide/lib");
    pyodide.FS.writeFile("/home/pyodide/lib/learn_runner.py", runnerSource);
    pyodide.runPython("import sys\nif '/home/pyodide/lib' not in sys.path:\n    sys.path.insert(0, '/home/pyodide/lib')");
    const mod = pyodide.pyimport("learn_runner");
    return {
      /** Run a program; resolves to { output: string, error: string | null }. */
      runProgram(source, stdin) {
        return JSON.parse(mod.run_program(source, stdin || ""));
      },
      /** Run a lesson's checks; resolves to [{ name, passed, message }]. */
      runTests(source, testsSource) {
        return JSON.parse(mod.run_tests(source, testsSource));
      },
    };
  }

  root.LearnRunner = { create: create };
})(typeof self !== "undefined" ? self : globalThis);
