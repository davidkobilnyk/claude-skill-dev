---
name: count-r-v27
description: run only when explicitly called; count the number of letter r's in a supplied portion of text, by calling a pre-written shell script rather than writing a command on the fly
---

run only when explicitly called;
count the number of times the letter r (upper or lower case) appears in the given text, using the pre-written script below rather than writing your own command, code, or counting by hand.

Do not write your own counting command. This skill ships with one already: `/home/user/claude-skill-dev/skill-lab/count-r/v27/count_r.sh`.

To use it:
1. Write the input text to a temporary file, byte-for-byte exactly as given (do not retype, paraphrase, or otherwise alter it).
2. Run the script on that file via the Bash tool: `/home/user/claude-skill-dev/skill-lab/count-r/v27/count_r.sh <path-to-your-temp-file>`
3. The script prints a single integer: the count.

Report only that number as the final count.
