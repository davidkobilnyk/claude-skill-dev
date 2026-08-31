---
name: dk-arithmetic-v1b
description: run only when explicitly called; evaluate a sequence of arithmetic operations given as text and output the correct numerical answer
---

# dk-arithmetic-v1b

Read the supplied text, find the arithmetic expression it describes, and compute the correct numerical answer using standard math rules. Output only the final numeric result.

If a division does not terminate cleanly, report the result as a decimal with a repeating-decimal indicator, e.g. `3.333... (10/3)`, showing both the repeating decimal and the exact fraction.

If the text contains no arithmetic to compute, output: `N/A - no arithmetic expression found`
