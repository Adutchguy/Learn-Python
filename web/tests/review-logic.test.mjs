import assert from "node:assert/strict";
import test from "node:test";

import {
  addDays,
  describeDay,
  dueQuestions,
  INTERVAL_DAYS,
  localDateString,
  nextDueDay,
  nextEntry,
  pickSession,
} from "../src/scripts/review-logic.ts";

const TODAY = "2026-11-06";

test("review: dates add correctly across month and year ends", () => {
  assert.equal(addDays("2026-11-06", 1), "2026-11-07");
  assert.equal(addDays("2026-11-30", 1), "2026-12-01");
  assert.equal(addDays("2026-12-31", 1), "2027-01-01");
  assert.equal(addDays("2028-02-28", 1), "2028-02-29"); // leap year
  assert.equal(addDays("2026-11-06", 30), "2026-12-06");
  assert.equal(localDateString(new Date(2026, 0, 5)), "2026-01-05");
});

test("review: a correct answer climbs one box and waits longer each time", () => {
  let entry = nextEntry(undefined, true, TODAY);
  assert.deepEqual(entry, { box: 1, due: "2026-11-07", seen: 1 });
  const waits = [];
  for (let i = 0; i < 5; i++) {
    entry = nextEntry(entry, true, TODAY);
    waits.push(entry.box);
  }
  assert.deepEqual(waits, [2, 3, 4, 5, 5], "the box stops at 5");
  assert.equal(entry.due, addDays(TODAY, INTERVAL_DAYS[5]), "the top box waits 30 days");
  assert.equal(entry.seen, 6);
});

test("review: a wrong answer drops the question to box 0, due tomorrow", () => {
  const entry = nextEntry({ box: 4, due: TODAY, seen: 7 }, false, TODAY);
  assert.deepEqual(entry, { box: 0, due: "2026-11-07", seen: 8 });
});

const questions = [
  { id: "a1", lesson: "m/1" },
  { id: "a2", lesson: "m/1" },
  { id: "b1", lesson: "m/2" },
  { id: "c1", lesson: "m/3" },
];

test("review: only questions from completed lessons are eligible", () => {
  const state = { completed: new Set(["m/1", "m/2"]), entries: {}, today: TODAY };
  assert.deepEqual(dueQuestions(questions, state).map((q) => q.id), ["a1", "a2", "b1"]);
  assert.deepEqual(dueQuestions(questions, { ...state, completed: new Set() }), []);
});

test("review: overdue questions come first (oldest first), then new ones; future ones are not due", () => {
  const state = {
    completed: new Set(["m/1", "m/2", "m/3"]),
    entries: {
      a1: { box: 2, due: "2026-11-05", seen: 2 },
      a2: { box: 3, due: "2026-11-09", seen: 3 },
      c1: { box: 1, due: "2026-11-01", seen: 1 },
    },
    today: TODAY,
  };
  assert.deepEqual(dueQuestions(questions, state).map((q) => q.id), ["c1", "a1", "b1"]);
  assert.equal(nextDueDay(questions, state), "2026-11-09");
});

test("review: a session is capped, and nothing scheduled means no next day", () => {
  const many = Array.from({ length: 25 }, (_, i) => ({ id: `q${i}`, lesson: "m/1" }));
  const state = { completed: new Set(["m/1"]), entries: {}, today: TODAY };
  assert.equal(pickSession(many, state).length, 10);
  assert.equal(pickSession(many, state, 3).length, 3);
  assert.equal(nextDueDay(many, state), null);
});

test("review: describing a day", () => {
  assert.equal(describeDay("2026-11-07", TODAY), "tomorrow");
  assert.match(describeDay("2026-11-20", TODAY), /^on /);
});
