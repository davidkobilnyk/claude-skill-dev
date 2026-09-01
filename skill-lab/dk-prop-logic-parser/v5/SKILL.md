---
name: dk-prop-logic-parser-v5
description: run only when explicitly called; convert English prose into formal propositional logic with consistent symbols, or say it's not valid propositional logic
---

# dk-prop-logic-parser-v5

Convert the given English prose into propositional logic. If it isn't a set of declarative, truth-apt claims combinable with and/or/not/if-then/iff — e.g. it quantifies over a class (including implicitly, without the word "all"), expresses modality/obligation, is a question, command, narrative, or empty — respond with `INVALID: <reason>` instead. A vague, subjective, or single-named-individual claim is still valid.

Assign each distinct proposition a capital letter in order of first appearance; reuse a symbol only for the exact same claim restated, never merely for shared vocabulary or a merely-correlated claim — when unsure whether two phrasings are the same claim, keep them separate.

Translate on logical relationship, not surface words. In particular: the antecedent of "if" is whichever clause follows "if," regardless of sentence order; "necessary for" and "sufficient for" point in opposite directions (A necessary for B ⟹ B→A; A sufficient for B ⟹ A→B); "only if" behaves like "necessary for," "provided that" like "sufficient for" reversed; "unless" (A unless B) ⟹ ¬B→A; a completed causal claim ("because X, Y" / "X caused Y") asserts both as true facts, not a conditional; "it is not the case that A and B" negates the whole expression, not each clause; a sentence bundling multiple claims needs full decomposition, not one merged atom.

Report the legend (symbol = proposition), then one formula per input sentence in input order.
