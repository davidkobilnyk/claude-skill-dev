---
name: count-r-v2
description: run only when explicitly called; count the number of letter r's in a supplied portion of text, via explicit character-by-character scanning
---

run only when explicitly called;
count the number of times the letter r (upper or lower case) appears in the given text.

Do not estimate. Go through the input one character at a time, from the first character to the last. Maintain a running count starting at 0. Each time the current character is "r" or "R", increment the count by 1. Ignore every other character (letters, spaces, punctuation, digits). After reaching the end of the input, report only the final count.
