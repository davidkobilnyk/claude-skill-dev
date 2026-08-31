---
name: dk-sum-v5
description: run only when explicitly called; add numbers and return the sum, preserving exact decimal precision
---

run only when explicitly called;
add numbers and return the sum

Do not round into a "cleaner" value (e.g. don't turn 0.999999999999999999999999 into 1.0). To avoid this:

1. Extract every number, however phrased ("+", "plus", "add", "and").
2. Find the max decimal places among the inputs — the answer must show exactly that many.
3. Add digit by digit, tracking every digit of every addend without approximating.
4. Before reporting, verify: does the last digit match true column-by-column addition? If not, redo it digit-by-digit.

Report the sum at the required precision, verified against the inputs.
