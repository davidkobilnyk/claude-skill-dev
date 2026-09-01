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

| Component | v1 | v2 | v3 | v4 | v5 | v6 | v7 | v8 | v9 | v10 | v11 | v12 | v13 | v14 | v15 | v16 | v17 | v18 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `validity-checklist` | ✓ | | | ✓ | | ✓ | ✓ | ✓ | ✓ | | | ✓ | ✓ | | ✓ | ✓ | ✓ | ✓ |
| `validity-principle` | | ✓ | | | ✓ | | | | | ✓ | | | | ✓ | | | | |
| `symtable-track` | ✓ | ✓ | ✓ (via examples) | ✓ | ✓ (brief) | ✓ | ✓ | ✓ | ✓ | ✓ (brief) | ✓ (via examples) | ✓ | ✓ | ✓ (via examples) | ✓ | ✓ | ✓ | ✓ |
| `paraphrase-merge-rule` | ✓ | ✓ | ✓ (via example C) | ✓ | ✓ (brief) | ✓ | ✓ | ✓ | ✓ | ✓ (brief) | ✓ (via example C) | **strengthened (H11)** | ✓ | ✓ (via example C) | ✓ | ✓ | ✓ | ✓ |
| `connective-map` | ✓ (table) | ✓ (prose) | ✓ (via examples) | ✓ (table) | ✓ (brief prose) | ✓ (table) | ✓ (table) | ✓ (table) | ✓ (table) | ✓ (brief prose) | ✓ (via examples) | ✓ (table) | ✓ (table) | ✓ (prose + examples) | ✓ (table) | ✓ (table) | ✓ (table) | ✓ (table) |
| `necsuff-rule` | ✓ | ✓ | ✓ (via example A) | ✓ | ✓ (brief) | removed (H6) | ✓ | ✓ | ✓ | ✓ (brief) | ✓ (via example A) | ✓ | ✓ | ✓ (via example A) | ✓ | ✓ | ✓ | ✓ |
| `negscope-rule` | ✓ | ✓ | ✓ (via example B) | ✓ | ✓ (brief) | ✓ | ✓ | ✓ | ✓ | ✓ (brief) | ✓ (via example B) | ✓ | ✓ | ✓ (via example B) | ✓ | ✓ | ✓ | ✓ |
| `causal-vs-cond` | ✓ | ✓ | ✓ (via example B) | ✓ | ✓ (brief) | ✓ | removed (H7) | ✓ | ✓ | ✓ (brief) | ✓ (via example B) | ✓ | **tightened (H18)** | ✓ (via example B) | ✓ | **re-qualified by completedness, not keyword (H22)** | ✓ | ✓ |
| `decompose-rule` | ✓ | ✓ | ✓ (via examples B, D) | ✓ | ✓ (brief) | ✓ | ✓ | removed (H9) | ✓ | ✓ (brief) | ✓ (via examples B, D) | ✓ | ✓ | ✓ (via examples B, D) | ✓ | ✓ | ✓ | ✓ |
| `scope-boundary` | ✓ | ✓ | | ✓ | | ✓ | ✓ | ✓ | removed (H10) | | | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `symbolic-detect` | ✓ | ✓ | ✓ (via example D) | ✓ | | ✓ | ✓ | ✓ | ✓ | | ✓ (via example D) | ✓ | ✓ | ✓ (via example D) | ✓ | ✓ | ✓ | ✓ |
| `inconsistency-detect` | ✓ | ✓ | ✓ (via example D) | ✓ | | ✓ | ✓ | ✓ | ✓ | added, more concrete (H2) | ✓ (via example D) | ✓ | ✓ | ✓ (via example D) | ✓ | ✓ | ✓ | ✓ |
| `injection-note` | ✓ (in checklist) | ✓ (in principle) | ✓ (in intro line) | ✓ (dedicated callout) | | ✓ (in checklist) | ✓ (in checklist) | ✓ (in checklist) | ✓ (in checklist) | | ✓ (in intro line) | ✓ (in checklist) | ✓ (in checklist) | ✓ (in principle) | ✓ (in checklist) | ✓ (in checklist) | ✓ (in checklist) | ✓ (in checklist) |
| `worked-example` | | | ✓ (4 examples) | ✓ (1 example) | | | | | | | **✓ (5 examples, H3)** | | | **✓ (4 examples, H21)** | | | | |
| `output-template` | ✓ | ✓ | ✓ | ✓ | ✓ (brief) | ✓ | ✓ | ✓ | ✓ | ✓ (brief) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `verify-step` | | ✓ | | ✓ | | | | | | | | | | ✓ | | | | |
| `subjective-inclusion-rule` | ✓ | ✓ | ✓ | ✓ | ✓ (brief) | ✓ | ✓ | ✓ | ✓ | ✓ (brief) | ✓ | ✓ | ✓ | ✓ | removed (H29) | ✓ | ✓ | ✓ |
| `alphabet-exhaustion-rule` | ✓ | ✓ | | | | ✓ | ✓ | ✓ | ✓ | | | ✓ | ✓ | | ✓ | ✓ | ✓ | removed (H28) |
| `argument-preserve` | ✓ | ✓ | | ✓ | | ✓ | ✓ | ✓ | ✓ | | | ✓ | ✓ | | ✓ | ✓ | removed (H27) | ✓ |

**Design axes Round 1 targeted:** checklist (v1) vs. principle (v2, v5) framing for validity; worked-examples-carry-the-rules (v3) vs. explicit-rules-stated-directly (v1, v2, v4); verify-step present (v2, v4) vs. absent (v1, v3, v5); maximal component coverage (v4) vs. minimal/lean (v5) as a brevity floor test.

**Round 2 targets:** each of v6/v7/v8/v9 is v1 with exactly one component removed (testing H6/H7/H9/H10 — is that component actually load-bearing, or is v1 over-specified?); v10 is v5 with one component strengthened (testing H2 — can v5's unreliable `inconsistency-detect` be made deterministic without losing its brevity edge?). v2, v3, v4, v5 are retired from the active set this round to fit the 6-variant cap (their Round 1 data stays on record; H3/H5, their diagnosed fixes, remain deferred, not abandoned).

**Round 3 targets:** picked via the `U × D × ln(rows+1)` prioritization score over the 15-item backlog (H3, H4, H5, H8, H11-H21) — see `HYPOTHESES.md` for the score derivation and the four selected. v11 (parent: v3) adds a 5th worked example teaching partial-validity extraction, testing H3. v12 (parent: v1) adds a paraphrase-merging bullet to Step 2, testing H11. v13 (parent: v1) replaces the full `causal-vs-cond` bullet with a tightened, shorter version naming the causal-verb sub-case specifically, testing H18. v14 (parent: v2 × v3, compound) merges v2's principle-based structure with v3's 4 worked examples as a distinct new section, testing H21 — see `HYPOTHESES.md` for why this is a compound hypothesis, not a bundle of already-isolated pieces.

**Round 4 targets:** picked via the same `U × D × ln(rows+1)` score over a fresh 20-hypothesis backlog. v15 (parent: v1) removes `subjective-inclusion-rule`'s guarding bullet, testing H29. v16 (parent: v1) re-qualifies `causal-vs-cond` by completedness/tense instead of naming a bare trigger keyword, testing H22 (a fix for v13's Round 3 regression, kept as a separate variant so v13's own tested history stays intact). v17 (parent: v1) removes `argument-preserve` entirely, testing H27. v18 (parent: v1) removes `alphabet-exhaustion-rule`'s specific overflow format instruction, testing H28. H25 (a fifth Round 4 hypothesis, about v12's generation-time cost) was resolved via re-analysis of already-collected data, no new variant.

## Scoring methodology notes

- Symbol *letters* are never scored literally — any consistent, injective relabeling of atoms counts as correct. Only connective structure, precedence/parenthesization, and atom-to-symbol consistency are graded.
- Judgment-call scenarios with more than one accepted answer (flagged inline in `tests.csv`'s `expected_output`): `either-or-ambiguity`, `negated-paraphrase`, `subjective-vague-claim`, `just-in-case-biconditional-idiom`, `single-word-fragment` (row a only). A variant matching any listed accepted reading, applied consistently, counts as correct on that row.
- `INVALID: <reason>` rows require the variant to decline conversion and state a reason in the same general category (exact wording is not required to match).
