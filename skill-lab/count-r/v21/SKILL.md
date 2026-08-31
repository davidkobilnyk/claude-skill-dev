---
name: count-r-v21
description: run only when explicitly called; count the number of letter r's in a supplied portion of text, using a short Python script with Unicode normalization instead of manual transcription
---

run only when explicitly called;
count the number of times the letter r (upper or lower case) appears in the given text, using code rather than manual counting.

Write and run a short Python script (via the available code-execution/Bash tool) that does the following:
1. Take the input text exactly as given.
2. Apply Unicode NFKD normalization to it (`unicodedata.normalize('NFKD', text)`). This decomposes stylized or decorative Unicode forms of a letter (for example, full-width, bold, italic, or superscript R) into their plain base letter, and also separates any diacritical mark (such as the caron in ř) from its base letter into two adjacent characters.
3. Walk through the normalized string one character at a time. Count a character as a match only if it is exactly "r" or "R" AND it is not immediately followed by a combining mark (check with `unicodedata.combining(ch) != 0`). A combining mark immediately after means the original character was a distinct letter with a diacritic (like ř), not a plain stylized r/R — skip it, and skip the combining mark(s) that follow it, rather than counting it.
4. Print the final count.

Run the script and report only the number it prints as the final count.
