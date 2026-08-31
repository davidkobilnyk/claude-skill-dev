---
name: count-r-v7
description: run only when explicitly called; count the number of letter r's in a supplied portion of text, via character-by-character scanning with an explicit warning about repeated-letter clusters
---

run only when explicitly called;
count the number of times the letter r (upper or lower case) appears in the given text.

Do not estimate. Go through the input one character at a time, from the first character to the last. Maintain a running count starting at 0. Each time the current character is "r" or "R", increment the count by 1 — this includes every single r in a row when several appear consecutively (e.g. "rr" is 2, not 1; "rrr" is 3, not 1) — never collapse a run of repeated r's into a single count. Ignore every other character (letters, spaces, punctuation, digits). After reaching the end of the input, report only the final count.
