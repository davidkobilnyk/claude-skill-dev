---
name: count-r-v23
description: run only when explicitly called; count the number of letter r's in a supplied portion of text, using a single grep/wc shell command instead of a Python script
---

run only when explicitly called;
count the number of times the letter r (upper or lower case) appears in the given text, using a single shell command rather than writing code, running a script file, or counting by hand.

Write the input text to a temporary file, byte-for-byte exactly as given (do not retype, paraphrase, or otherwise alter it). Then run this exact command via the Bash tool:

LC_ALL=C.UTF-8 grep -oP '[rRＲｒ𝐑𝐫𝑅ʳ]' <path-to-your-temp-file> | wc -l

Setting LC_ALL=C.UTF-8 is required — without an explicit UTF-8 locale, grep can silently return incorrect results on non-ASCII input rather than erroring. The character class matches plain "r"/"R" plus their stylized Unicode variants (fullwidth, mathematical bold, superscript), while correctly excluding genuinely different letters such as ř (r with a diacritical mark), which are not in the class.

Report only the number that command prints as the final count.
