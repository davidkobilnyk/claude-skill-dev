---
name: count-r-v28
description: run only when explicitly called; count the number of letter r's in a supplied portion of text, by calling a pre-written shell script, falling back to manual counting only if the script is unavailable
---

run only when explicitly called;
count the number of times the letter r (upper or lower case) appears in the given text.

## Primary method: pre-written script

This skill ships with a script already written: `/home/user/claude-skill-dev/skill-lab/count-r/v28/count_r.sh`. Prefer this method whenever it works.

1. Write the input text to a temporary file, byte-for-byte exactly as given (do not retype, paraphrase, or otherwise alter it).
2. Run the script on that file via the Bash tool: `/home/user/claude-skill-dev/skill-lab/count-r/v28/count_r.sh <path-to-your-temp-file>`
3. If it runs successfully and prints a single integer, report that number as the final count and stop here — do not also do the manual method below.

## Fallback method: only if the script above is unavailable or fails to run

If the script cannot be found, cannot be executed, or errors out for any reason (for example: no file access, no shell/code execution available in this environment), do not just report failure — fall back to counting manually instead, using this procedure:

First, rewrite the entire input as a hyphen-separated sequence of its individual characters. Write this full sequence out before counting anything. Then count how many items in that sequence are "r" or "R" — this includes any character that is a stylized or decorative Unicode form of the same letter (for example: full-width, bold, italic, or superscript variants), even though its exact character code differs from plain ASCII r/R. Do not count a character that represents a genuinely different letter, such as one from a non-Latin alphabet or one carrying a diacritical mark (for example ř), even if it looks similar to r — a different letter is not a match, no matter how visually close.

Before reporting, verify your work: count the total number of items in your hyphenated sequence and confirm it matches the length of the original input exactly.

Report the final, verified count, and note that you used the manual fallback method because the script was unavailable.
