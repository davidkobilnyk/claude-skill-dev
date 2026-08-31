---
name: dk-sum-v6
description: run only when explicitly called; add numbers and return the sum, preserving exact decimal precision
---

run only when explicitly called;
add numbers and return the sum

Don't round into a "cleaner" value (e.g. 0.999999999999999999999999 must not become 1.0).

1. Find the max decimal places among the inputs — the answer must show exactly that many digits.
2. Add digit by digit, without approximating any addend.
3. Verify the last digit against true column addition before reporting; redo if it doesn't match.
