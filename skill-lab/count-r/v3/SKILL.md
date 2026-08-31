---
name: count-r-v3
description: run only when explicitly called; count the number of letter r's in a supplied portion of text, by first spelling the text out character by character
---

run only when explicitly called;
count the number of times the letter r (upper or lower case) appears in the given text.

First, rewrite the entire input as a hyphen-separated sequence of its individual characters (for example, "bar" becomes b-a-r; keep spaces and punctuation as their own items too). Write this full sequence out before counting anything. Then count how many items in that sequence are "r" or "R". Report only the final count.
