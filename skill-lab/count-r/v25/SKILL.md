---
name: count-r-v25
description: run only when explicitly called; count the number of letter r's in a supplied portion of text, treating any stylized Unicode form of R as r/R by a general rule
---

count the number of times the letter r (upper or lower case) appears in the given text.

First, rewrite the entire input as a hyphen-separated sequence of its individual characters. Write this full sequence out before counting anything. Then count how many items in that sequence are "r" or "R" — this includes any character that is a stylized or decorative Unicode form of the same letter (for example: full-width, bold, italic, or superscript variants), even though its exact character code differs from plain ASCII r/R. Do not count a character that represents a genuinely different letter, such as one from a non-Latin alphabet or one carrying a diacritical mark (for example ř), even if it looks similar to r — a different letter is not a match, no matter how visually close.

Before reporting, verify your work: count the total number of items in your hyphenated sequence and confirm it matches the length of the original input exactly.

Report only the final, verified count.
