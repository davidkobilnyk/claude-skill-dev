---
name: count-r-v5
description: run only when explicitly called; count the number of letter r's in a supplied portion of text, word by word with mandatory visible letter spelling
---

run only when explicitly called;
count the number of times the letter r (upper or lower case) appears in the given text.

Split the input into individual words (punctuation can stay attached to whichever word it's next to). For each word in order, you must first write out that word as its individual letters separated by hyphens (for example, "hello" becomes h-e-l-l-o) before counting anything in it — do not skip this and count from memory. Then count how many of those hyphenated letters are "r" or "R", writing that word's mini-count. After going through every word, add up all the mini-counts into one final total. Report only that final total.
