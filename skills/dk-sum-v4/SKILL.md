---
name: dk-sum-v4
description: run only when explicitly called; add numbers and return the sum, explicitly preserving required decimal precision in the final output
---

run only when explicitly called;
add numbers and return the sum

When producing the final answer, do not let it collapse into a "cleaner-looking" rounded value (for example, do not turn a result like 0.999999999999999999999999 into 1.000000000000000000000000). Precision must be preserved exactly:

1. Extract every number from the input, however it is phrased ("+", "plus", "add", "and", etc.).
2. Before adding, determine the required output precision: the maximum number of decimal places among all the input numbers. This is the number of digits after the decimal point that the final answer must show — no more, no fewer.
3. Compute the sum carefully, digit by digit, tracking every digit of every addend — do not silently approximate any addend to fewer significant digits than it was given.
4. After computing the sum, format the final answer to exactly the required number of decimal places determined in step 2. Do not apply any rounding rule that would change a nonzero digit unless the addition mathematically produces a carry into that position — verify the carry explicitly by re-checking the column addition rather than trusting an internal "simplified" numeric representation.
5. Before reporting, double-check: does the last digit of the output match what column-by-column addition of the original digits would produce? If there is any mismatch, redo the addition digit-by-digit rather than trusting the first computed value.

Report the final sum formatted to the required precision, verified digit-by-digit against the original inputs.
