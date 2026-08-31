---
name: count-r-v6
description: run only when explicitly called; count the number of letter r's in a supplied portion of text, by spelling it out then verifying the transcription and count
---

run only when explicitly called;
count the number of times the letter r (upper or lower case) appears in the given text.

First, rewrite the entire input as a hyphen-separated sequence of its individual characters (for example, "bar" becomes b-a-r; keep spaces and punctuation as their own items too). Write this full sequence out before counting anything. Then count how many items in that sequence are "r" or "R".

Before reporting, verify your work: count the total number of items in your hyphenated sequence and confirm it matches the length of the original input exactly — if it doesn't, you made a transcription error, so redo the spelling from scratch. Then recount the "r"/"R" items a second time, independently, and use that second count only if it disagrees with the first; if the two counts disagree, redo the count until two consecutive counts agree.

Report only the final, verified count.
