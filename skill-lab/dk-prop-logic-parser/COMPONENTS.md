# Components — dk-prop-logic-parser

Atomic building blocks a variant's instruction text can include. Each gets a short ID used in `HYPOTHESES.md` and the table below.

## Component inventory

- **`validity-checklist`** — an enumerated list of disqualifying categories (quantifiers, modal, temporal, imperative, interrogative, narrative, non-English, empty/fragment) to check before attempting conversion.
- **`validity-principle`** — the same disqualification logic stated as a general principle ("must be a declarative, truth-apt claim with no quantifiers, modal/temporal operators, or missing propositional content") rather than an enumerated list.
- **`symtable-track`** — explicit instruction to build and maintain a running symbol legend across all sentences in a set, checking each new sentence against the existing table before assigning a new letter.
- **`paraphrase-merge-rule`** — explicit rule for when two differently-worded sentences should merge into the same symbol vs. stay distinct: merge only on near-certain equivalence, never on mere word overlap (guards against the false-paraphrase and equivocation traps).
- **`connective-map`** — an explicit mapping table/list from English phrases (including implicit ones: unless, only if, provided that, neither/nor, just in case) to logical connectives.
- **`necsuff-rule`** — a dedicated rule specifically for "necessary for" / "sufficient for" phrasing and which direction each implies.
- **`negscope-rule`** — explicit rule for preserving negation scope in "it is not the case that X and Y" style phrasing (De Morgan scope, not naive per-clause negation).
- **`causal-vs-cond`** — explicit rule distinguishing causal assertions about completed events (render as conjunction, both true) from genuine hypothetical conditionals (render as implication).
- **`decompose-rule`** — explicit instruction to decompose a sentence bundling multiple independent clauses into separate atomic propositions rather than treating the whole compound as one atom.
- **`scope-boundary`** — explicit rule for resetting symbol scope across multiple independent example/set blocks within one input.
- **`symbolic-detect`** — explicit step to detect input that's already (partially) in symbolic notation (Unicode or ASCII pseudo-notation) and normalize/pass through rather than re-deriving from English.
- **`inconsistency-detect`** — explicit instruction to detect and resolve inconsistent symbol reuse within the input itself (a letter redefined mid-text) by introducing a new symbol for the second sense.
- **`injection-note`** — explicit instruction to treat embedded meta-instructions/prompt-injection-shaped text as ordinary content to exclude from formalization, not as a command to follow.
- **`worked-example`** — one or more full worked examples embedded in the skill text demonstrating input → legend → formula end to end.
- **`output-template`** — a strict, spelled-out required output format (legend block + formula list) vs. leaving format loose.
- **`verify-step`** — an explicit final self-check: every symbol used in a formula appears in the legend exactly once, and every atomic proposition maps to exactly one symbol.
- **`subjective-inclusion-rule`** — explicit rule that subjective/vague declarative sentences still count as valid atomic propositions, guarding against over-flagging them invalid.
- **`alphabet-exhaustion-rule`** — explicit instruction for what to do past 26 distinct propositions (subscripted symbols, e.g. P1, P2, ...).
- **`argument-preserve`** — explicit instruction to preserve premise/conclusion labeling when the input is structured as a labeled argument, rather than flattening it to an unordered statement list.

## Components × variants

| Component | v1 | v2 | v3 | v4 | v5 | v6 | v7 | v8 | v9 | v10 |
|---|---|---|---|---|---|---|---|---|---|---|
| `validity-checklist` | ✓ | | | ✓ | | ✓ | ✓ | ✓ | ✓ | |
| `validity-principle` | | ✓ | | | ✓ | | | | | ✓ |
| `symtable-track` | ✓ | ✓ | ✓ (via examples) | ✓ | ✓ (brief) | ✓ | ✓ | ✓ | ✓ | ✓ (brief) |
| `paraphrase-merge-rule` | ✓ | ✓ | ✓ (via example C) | ✓ | ✓ (brief) | ✓ | ✓ | ✓ | ✓ | ✓ (brief) |
| `connective-map` | ✓ (table) | ✓ (prose) | ✓ (via examples) | ✓ (table) | ✓ (brief prose) | ✓ (table) | ✓ (table) | ✓ (table) | ✓ (table) | ✓ (brief prose) |
| `necsuff-rule` | ✓ | ✓ | ✓ (via example A) | ✓ | ✓ (brief) | **removed (H6)** | ✓ | ✓ | ✓ | ✓ (brief) |
| `negscope-rule` | ✓ | ✓ | ✓ (via example B) | ✓ | ✓ (brief) | ✓ | ✓ | ✓ | ✓ | ✓ (brief) |
| `causal-vs-cond` | ✓ | ✓ | ✓ (via example B) | ✓ | ✓ (brief) | ✓ | **removed (H7)** | ✓ | ✓ | ✓ (brief) |
| `decompose-rule` | ✓ | ✓ | ✓ (via examples B, D) | ✓ | ✓ (brief) | ✓ | ✓ | **removed (H9)** | ✓ | ✓ (brief) |
| `scope-boundary` | ✓ | ✓ | | ✓ | | ✓ | ✓ | ✓ | **removed (H10)** | |
| `symbolic-detect` | ✓ | ✓ | ✓ (via example D) | ✓ | | ✓ | ✓ | ✓ | ✓ | |
| `inconsistency-detect` | ✓ | ✓ | ✓ (via example D) | ✓ | | ✓ | ✓ | ✓ | ✓ | **added, more concrete (H2)** |
| `injection-note` | ✓ (in checklist) | ✓ (in principle) | ✓ (in intro line) | ✓ (dedicated callout) | | ✓ (in checklist) | ✓ (in checklist) | ✓ (in checklist) | ✓ (in checklist) | |
| `worked-example` | | | ✓ (4 examples) | ✓ (1 example) | | | | | | |
| `output-template` | ✓ | ✓ | ✓ | ✓ | ✓ (brief) | ✓ | ✓ | ✓ | ✓ | ✓ (brief) |
| `verify-step` | | ✓ | | ✓ | | | | | | |
| `subjective-inclusion-rule` | ✓ | ✓ | ✓ | ✓ | ✓ (brief) | ✓ | ✓ | ✓ | ✓ | ✓ (brief) |
| `alphabet-exhaustion-rule` | ✓ | ✓ | | | | ✓ | ✓ | ✓ | ✓ | |
| `argument-preserve` | ✓ | ✓ | | ✓ | | ✓ | ✓ | ✓ | ✓ | |

**Design axes Round 1 targeted:** checklist (v1) vs. principle (v2, v5) framing for validity; worked-examples-carry-the-rules (v3) vs. explicit-rules-stated-directly (v1, v2, v4); verify-step present (v2, v4) vs. absent (v1, v3, v5); maximal component coverage (v4) vs. minimal/lean (v5) as a brevity floor test.

**Round 2 targets:** each of v6/v7/v8/v9 is v1 with exactly one component removed (testing H6/H7/H9/H10 — is that component actually load-bearing, or is v1 over-specified?); v10 is v5 with one component strengthened (testing H2 — can v5's unreliable `inconsistency-detect` be made deterministic without losing its brevity edge?). v2, v3, v4, v5 are retired from the active set this round to fit the 6-variant cap (their Round 1 data stays on record; H3/H5, their diagnosed fixes, remain deferred, not abandoned).

## Scoring methodology notes

- Symbol *letters* are never scored literally — any consistent, injective relabeling of atoms counts as correct. Only connective structure, precedence/parenthesization, and atom-to-symbol consistency are graded.
- Judgment-call scenarios with more than one accepted answer (flagged inline in `tests.csv`'s `expected_output`): `either-or-ambiguity`, `negated-paraphrase`, `subjective-vague-claim`, `just-in-case-biconditional-idiom`, `single-word-fragment` (row a only). A variant matching any listed accepted reading, applied consistently, counts as correct on that row.
- `INVALID: <reason>` rows require the variant to decline conversion and state a reason in the same general category (exact wording is not required to match).
