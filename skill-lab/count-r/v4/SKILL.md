---
name: count-r-v4
description: run only when explicitly called; count the number of letter r's in a supplied portion of text, by tallying word by word
---

run only when explicitly called;
count the number of times the letter r (upper or lower case) appears in the given text.

Split the input into individual words (punctuation can stay attached to whichever word it's next to). For each word in order, spell it out and count how many of its letters are "r" or "R", writing that word's mini-count. After going through every word, add up all the mini-counts into one final total. Report only that final total.
