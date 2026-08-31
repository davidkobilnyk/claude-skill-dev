---
name: count-r-v10
description: run only when explicitly called; count the number of letter r's in a supplied portion of text, via character-by-character scanning with a repeated-letter warning and a final re-scan check
---

run only when explicitly called;
count the number of times the letter r (upper or lower case) appears in the given text.

Do not estimate. Go through the input one character at a time, from the first character to the last. Maintain a running count starting at 0. Each time the current character is "r" or "R", increment the count by 1 — this includes every single r in a row when several appear consecutively (e.g. "rr" is 2, not 1; "rrr" is 3, not 1) — never collapse a run of repeated r's into a single count. Ignore every other character (letters, spaces, punctuation, digits).

Before reporting, re-scan the entire input one more time from the start, counting again independently. If the two scans disagree, scan a third time and use whichever count two of the three scans agree on.

Report only the final count.
