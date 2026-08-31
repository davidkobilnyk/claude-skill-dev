# count-r hypotheses log

Tracks, per new variant: the hypothesis it tests, the change made, and (after the next run) the result and lesson learned.

## Round 1 results summary (v1-v4, 12-case suite)

- v1 (baseline, 278 chars): 7/12. Failed on "hello" (hallucinated an r), "Mirror"/"irregular"/"Rrrrr" (all undercounted double-letter clusters), and the R2D2 stress case (overcounted).
- v2 (char-by-char scan, 650 chars): 9/12. Failed on "hello" (hallucinated) and "Mirror"/"irregular" (undercounted clusters). Fixed the stress case v1 missed.
- v3 (spell-out-then-count, 633 chars): 9/12. Fixed "hello" and "Mirror" (the spelling step eliminated the hallucination). Failed by mis-transcribing "Rrrrr" (wrote 6 chars instead of 5) and "purrrring" (dropped an r), and by miscounting its own correct spelling of "irregular" (said 2 instead of 3).
- v4 (word-by-word tally, 613 chars): 10/12, best of the round. Fixed all cluster-undercount cases (Mirror, irregular, Rrrrr, RRRR) via per-word decomposition. Still failed "hello" (hallucinated) and the plain sentence test (likely an aggregation error summing per-word tallies).

## count-r-v5 (parent: count-r-v4)
Hypothesis: v4's instructions already say to "spell it out" per word, but its failure on "hello" (and the fact that its reported outputs for simple words didn't visibly show the letter-by-letter spelling) suggests that step was being treated as optional/skippable rather than actually performed. Making the spell-out step mandatory and requiring it to appear in the visible output (not just described as an aside) should close that gap without reintroducing v3's cluster-transcription errors, since each word here is spelled in isolation rather than a full sentence.
Change made: reworded the per-word instruction from "spell it out and count" to an explicit mandatory instruction: "you must first write out that word as its individual letters separated by hyphens... before counting anything in it — do not skip this and count from memory."
Result: REFUTED. Scored 10/12. Still failed "hello": it correctly spelled h-e-l-l-o but then mis-totaled it as 1 anyway (a labeling/arithmetic slip downstream of correct spelling, not a spelling failure). It also reintroduced a cluster-transcription error on "Rrrrr" (wrote 6 characters instead of 5) that v4 itself did not have.
Lesson: mandatory visible spelling does not guarantee the count derived from that spelling is correct — the counting step itself needs its own safeguard. Forcing spelling on a repeated-letter word can itself introduce a transcription error, echoing v3's failure mode. Spelling alone, without verification, is not sufficient.

## count-r-v6 (parent: count-r-v3)
Hypothesis: v3's two demonstrated failure modes — mis-transcribing a run of repeated letters when spelling out the input (Rrrrr, purrrring), and miscounting its own correct spelling (irregular) — can both be caught by an explicit verification step: checking the spelled-out sequence's length against the original input's length (catches transcription drift), and recounting the r's a second time independently (catches counting slips).
Change made: added one verification paragraph after the existing spell-then-count instructions, requiring a length check and a second independent recount before reporting.
Result: CONFIRMED, strongly. Scored 12/12 — a clean sweep. Fixed all three of v3's demonstrated failure modes in this run (Rrrrr and purrrring transcription errors, and the irregular counting-after-correct-spelling slip) and also got "hello" right.
Lesson: an explicit verification/recount step is the most effective fix found so far for both transcription errors and counting-after-correct-spelling errors — more effective than the raw spell-out step alone (v3) or making spelling mandatory alone (v5). It comes at the highest character cost of any variant (1102), so it wins on correctness but loses the brevity tiebreak to v4 (613 chars, also 12/12).

## count-r-v7 (parent: count-r-v2)
Hypothesis: v2's undercounts on "Mirror" and "irregular" (both containing a double "rr") suggest the running character-by-character count sometimes treats a consecutive repeated letter as a single occurrence rather than counting each one. An explicit warning against collapsing repeated-letter runs, with a concrete example, should fix this without the heavier restructuring of v3/v4.
Change made: inserted one clause into the character-scanning instruction explicitly stating that consecutive r's must each be counted separately, with a worked example ("rr" is 2, not 1).
Result: CONFIRMED. Scored 11/12 — fixed exactly the two cluster-undercount cases it targeted (Mirror, irregular). Its only remaining failure was "hello", a different, unaddressed failure mode (the hallucination-type miscount that also hit v1, v2, v3, and v5 at least once).
Lesson: a small, narrowly-scoped textual addition can reliably fix a specific, mechanistically-understood failure mode without needing v3/v6's heavier spell-out-and-verify machinery. Targeted fixes beat wholesale rewrites when the failure mode is well understood.

## Round 2 results summary (v1-v7, 12-case suite, re-run with v5/v6/v7 added)

| Variant | Chars | Score |
|---|---:|---:|
| v1 | 278 | 7/12 |
| v2 | 650 | 9/12 |
| v3 | 633 | 9/12 |
| **v4** | **613** | **12/12** |
| v5 | 839 | 10/12 |
| **v6** | **1102** | **12/12** |
| v7 | 877 | 11/12 |

v4 and v6 tie on correctness at 12/12; v4 wins the brevity tiebreak decisively (613 vs 1102 chars) and is the best result in the experiment on both axes combined.

**Observed non-determinism**: v1, v2, and v3 (unchanged since round 1) each showed a *different* specific set of failures between round 1 and round 2 — e.g. v2 fixed "hello"/"irregular" this round but newly failed the sentence test and the R2D2 stress case; v3 newly failed "hello" this round despite fixing it in round 1. This confirms borderline pass/fail results are genuinely noisy from run to run and shouldn't be treated as a stable property of a variant without repeated evidence.

## Retirements after round 2

- **v1, v2, v3**: retired by user judgment call (not strict domination) — v1 was the worst performer both rounds and has nothing more to teach as the plain baseline; v2 and v3 were consistently second-to-last both rounds and each now has a child variant (v7, v6 respectively) that clearly outperforms it.
- **v5**: retired under the strict rule — dominated on *both* axes by v4 (613 chars/12/12 vs v5's 839 chars/10/12).

Files are kept in the repo for all four; they are simply excluded from future run matrices.

Active going into round 3: v4, v6, v7, plus v8/v9/v10 below (6 total, at cap).

## count-r-v8 (parent: count-r-v6)
Hypothesis: v6's verification block has two separable sub-steps — a length-check (transcribed sequence length == original input length) and an independent second recount. The recount alone may already be doing most of the work of catching counting-after-correct-spelling slips (like "irregular"), independent of the length-check, which more specifically targets transcription drift (like "Rrrrr"/"purrrring"). Removing the length-check should reveal whether v6's 12/12 score depends on it or not.
Change made: deleted the length-check sentence from v6; kept only the independent-recount instruction.
Result: (fill in after the next run: confirmed / refuted / inconclusive)
Lesson: (fill in after the next run)

## count-r-v9 (parent: count-r-v6)
Hypothesis: conversely, the length-check may be the more load-bearing of the two sub-steps — confirming the transcribed sequence's length matches the input's length forces careful re-transcription and may already catch most errors, making the separate independent recount redundant.
Change made: deleted the independent-recount instruction from v6; kept only the length-check.
Result: (fill in after the next run: confirmed / refuted / inconclusive)
Lesson: (fill in after the next run)

## count-r-v10 (parent: count-r-v7)
Hypothesis: v7 (877 chars, 11/12 in round 2) still fails "hello" — a hallucinated r on a zero-r word, the one failure mode its cluster-warning fix didn't target. A lightweight final re-scan (re-run the character-by-character count a second time and use majority agreement) might catch this hallucination without inheriting v6/v8/v9's heavier spell-out-and-verify mechanism.
Change made: added a re-scan-and-compare step (scan twice; on disagreement, scan a third time and take the majority) to v7's existing character-scanning instructions.
Result: (fill in after the next run: confirmed / refuted / inconclusive)
Lesson: (fill in after the next run)
