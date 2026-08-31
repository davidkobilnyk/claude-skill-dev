---
name: count-r-v24
description: run only when explicitly called; count the number of letter r's in a supplied portion of text, by building a complete character-frequency tally rather than scanning for r's specifically
---

run only when explicitly called;
count the number of times the letter r (upper or lower case) appears in the given text.

Build a complete frequency tally of the input: go through the text one character at a time, from first to last, and add each character to a running tally of how many times every distinct character has appeared so far. Account for every single character in the input exactly once — including spaces, punctuation, digits, and any other symbols — not just the ones that look like they might be r's. Treat any character that is a stylized or decorative Unicode form of the letter r (for example: full-width, bold, italic, or superscript variants) as the same tally entry as plain r/R, even though its exact character code differs. Do not merge a character that represents a genuinely different letter into the r/R tally entry, such as one from a non-Latin alphabet or one carrying a diacritical mark (for example ř), even if it looks similar to r — a different letter gets its own separate tally entry.

Before reporting, verify your work: sum the counts across every tally entry and confirm the total equals the length of the original input exactly — if it doesn't, you missed or double-counted a character, so redo the tally from scratch.

Report only the final tally count for r/R (combined with its stylized variants as described above).
