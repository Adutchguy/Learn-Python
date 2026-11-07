// Dark theme for the code editor. Every colour here is at least 4.5:1 against the
// editor background (WCAG AA); the stock one-dark theme falls below that for comments
// and line numbers. Light mode uses CodeMirror's default styling, which already passes.
import { EditorView } from "@codemirror/view";
import { HighlightStyle, syntaxHighlighting } from "@codemirror/language";
import { tags as t } from "@lezer/highlight";

const bg = "#0f141b";
const text = "#e6ebf2";
const muted = "#a5b1c2";
const selection = "#2d4a6d";

const theme = EditorView.theme(
  {
    "&": { color: text, backgroundColor: bg },
    ".cm-content": { caretColor: "#ffffff" },
    ".cm-cursor, .cm-dropCursor": { borderLeftColor: "#ffffff" },
    "&.cm-focused > .cm-scroller > .cm-selectionLayer .cm-selectionBackground, .cm-selectionBackground, .cm-content ::selection":
      { backgroundColor: selection },
    ".cm-activeLine": { backgroundColor: "#18202b" },
    ".cm-gutters": { backgroundColor: bg, color: muted, border: "none" },
    ".cm-activeLineGutter": { backgroundColor: "#18202b", color: text },
    ".cm-panels": { backgroundColor: "#18202b", color: text },
    ".cm-tooltip": { backgroundColor: "#18202b", color: text, border: "1px solid #2b3645" },
  },
  { dark: true },
);

const highlight = HighlightStyle.define([
  { tag: [t.keyword, t.controlKeyword, t.operatorKeyword, t.definitionKeyword, t.moduleKeyword], color: "#e5a3ff" },
  { tag: [t.string, t.special(t.string)], color: "#9fe0a0" },
  { tag: [t.number, t.bool, t.null], color: "#ffb86b" },
  { tag: [t.comment, t.lineComment, t.blockComment], color: muted, fontStyle: "italic" },
  { tag: [t.function(t.variableName), t.function(t.propertyName), t.definition(t.variableName)], color: "#7cc4ff" },
  { tag: [t.className, t.typeName], color: "#ffd479" },
  { tag: [t.propertyName, t.attributeName], color: "#7cc4ff" },
  { tag: [t.operator, t.punctuation], color: text },
  { tag: t.invalid, color: "#ff8a80" },
]);

export const accessibleDark = [theme, syntaxHighlighting(highlight)];
