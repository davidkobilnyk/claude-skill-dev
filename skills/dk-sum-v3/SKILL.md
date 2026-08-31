---
name: dk-sum-v3
description: run only when explicitly called; add numbers and return the sum, using exact integer/fixed-point arithmetic to avoid floating-point precision loss
---

run only when explicitly called;
add numbers and return the sum

Do not add the numbers as ordinary floating-point values. Instead, convert the addition into exact integer arithmetic:

1. Extract every number from the input, however it is phrased ("+", "plus", "add", "and", etc.).
2. Find the maximum number of decimal places, N, across all the numbers (a number with no decimal point has 0 decimal places).
3. Convert every number into an integer by multiplying it by 10^N (i.e., shift the decimal point N places to the right, padding with trailing zeros as needed). These are now exact integers with no fractional part.
4. Add all the resulting integers together using exact integer addition — this has no rounding error regardless of how many digits are involved.
5. Convert the integer sum back into a decimal number by dividing by 10^N (i.e., re-insert the decimal point N places from the right).
6. Strip only trailing zeros that are not needed for precision; never round or drop a nonzero digit.

Report the final sum as this exact reconstructed decimal value, not a value computed or reformatted through ordinary floating-point math.
