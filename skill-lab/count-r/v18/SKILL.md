---
name: count-r-v18
description: run only when explicitly called; count the number of letter r's in a supplied portion of text, treating an explicit list of stylized Unicode R variants as r/R
---

run only when explicitly called;
count the number of times the letter r (upper or lower case) appears in the given text.

First, rewrite the entire input as a hyphen-separated sequence of its individual characters (for example, "bar" becomes b-a-r; keep spaces and punctuation as their own items too). Write this full sequence out before counting anything. Then count how many items in that sequence are "r" or "R" — this includes the following stylized Unicode variants of the letter R, which also count as a match: fullwidth Ｒ and ｒ, mathematical bold 𝐑 and 𝐫, mathematical italic 𝑅, and modifier letter small ʳ. Do not count a letter from a different alphabet, or a letter with a diacritical mark (such as ř), even if it looks similar — those are a different letter, not r/R.

Before reporting, verify your work: count the total number of items in your hyphenated sequence and confirm it matches the length of the original input exactly — if it doesn't, you made a transcription error, so redo the spelling from scratch.

Report only the final, verified count.
