---
name: dk-sum-v2
description: run only when explicitly called; add numbers and return the sum, using exact digit-by-digit decimal addition to avoid floating-point precision loss
---

run only when explicitly called;
add numbers and return the sum

Do not compute the sum by treating the numbers as ordinary floating-point values. Instead, add them the way you would by hand on paper, using exact decimal digit arithmetic:

1. Extract every number from the input, however it is phrased ("+", "plus", "add", "and", etc.).
2. Line up all numbers on their decimal point. Treat any number without an explicit decimal point as having zero decimal places.
3. Pad each number on the right with trailing zeros so every number has the same number of decimal places as the number with the most decimal places.
4. Add the digits column by column from right to left, exactly as in grade-school long addition, carrying into the next column as needed. Do not round or truncate any digit at any step.
5. Place the decimal point in the result at the same position as in the padded addends.
6. Strip only the trailing zeros that are not needed for precision, but never drop or round a nonzero digit.

Report the final sum as the exact digit string produced by this process, not a value that has been reformatted or rounded by ordinary floating-point math.
