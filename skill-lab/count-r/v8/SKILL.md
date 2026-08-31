---
name: count-r-v8
description: run only when explicitly called; count the number of letter r's in a supplied portion of text, by spelling it out then recounting to verify
---

run only when explicitly called;
count the number of times the letter r (upper or lower case) appears in the given text.

First, rewrite the entire input as a hyphen-separated sequence of its individual characters (for example, "bar" becomes b-a-r; keep spaces and punctuation as their own items too). Write this full sequence out before counting anything. Then count how many items in that sequence are "r" or "R".

Before reporting, recount the "r"/"R" items a second time, independently, and use that second count only if it disagrees with the first; if the two counts disagree, redo the count until two consecutive counts agree.

Report only the final, verified count.
