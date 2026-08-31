---
name: count-r-v20
description: run only when explicitly called; count the number of letter r's in a supplied portion of text, explicitly flagging and resolving any non-standard characters before counting
---

run only when explicitly called;
count the number of times the letter r (upper or lower case) appears in the given text.

First, rewrite the entire input as a hyphen-separated sequence of its individual characters (for example, "bar" becomes b-a-r; keep spaces and punctuation as their own items too). Write this full sequence out before counting anything.

Next, scan the sequence for any item that is not a plain ASCII letter, digit, space, or common punctuation mark. For each such item, explicitly state whether it represents the letter r or R in a stylized or decorative form (for example, a full-width, bold, or superscript R — count these as r/R) or whether it is a genuinely different letter (for example, one with a diacritical mark, or a letter from a different alphabet — do not count these). If there are no such items, state that and move on.

Then count how many items in the sequence are "r"/"R" or one of the stylized variants you identified as a match above.

Before reporting, verify your work: count the total number of items in your hyphenated sequence and confirm it matches the length of the original input exactly — if it doesn't, you made a transcription error, so redo the spelling from scratch.

Report only the final, verified count.
