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
Result: REFUTED. Scored 9/12. Removing the length-check reintroduced exactly the transcription errors it was meant to catch: mis-transcribed "Rrrrr" as 6 characters and dropped an r from "purrrring" — the same failure modes v3 originally had, before v6 fixed them. Also picked up an unrelated new miscount on the plain sentence test.
Lesson: the recount alone is not sufficient to prevent transcription drift on inputs with repeated-letter runs. The length-check specifically targets that failure mode and the recount does not substitute for it.

## count-r-v9 (parent: count-r-v6)
Hypothesis: conversely, the length-check may be the more load-bearing of the two sub-steps — confirming the transcribed sequence's length matches the input's length forces careful re-transcription and may already catch most errors, making the separate independent recount redundant.
Change made: deleted the independent-recount instruction from v6; kept only the length-check.
Result: CONFIRMED, strongly. Scored 12/12 — a clean sweep, including correctly transcribing both "Rrrrr" and "purrrring" (the exact cases v8 got wrong without the length-check). Achieved this at 896 chars, beating v6's own 1102 chars for equal-or-better correctness in this round.
Lesson: the length-check is the load-bearing half of v6's verification step; the independent recount was largely redundant. v9 is now the strongest correctness/brevity combination found in the experiment — pending replication, since no variant (including v6 and v4, both perfect in round 2) has scored perfectly on two consecutive rounds yet.

## count-r-v10 (parent: count-r-v7)
Hypothesis: v7 (877 chars, 11/12 in round 2) still fails "hello" — a hallucinated r on a zero-r word, the one failure mode its cluster-warning fix didn't target. A lightweight final re-scan (re-run the character-by-character count a second time and use majority agreement) might catch this hallucination without inheriting v6/v8/v9's heavier spell-out-and-verify mechanism.
Change made: added a re-scan-and-compare step (scan twice; on disagreement, scan a third time and take the majority) to v7's existing character-scanning instructions.
Result: REFUTED. Scored 9/12, no better than v7's own 9/12 this round, and still failed "hello". Also failed "Mirror" (reasoned to 3, reported final answer as 2 — a transcription-to-final-answer slip, not a counting error) and "irregular" (new failure, got 2 instead of 3).
Lesson: a bare re-scan-and-majority-vote, without externalizing the character sequence first (as v6/v9's spell-out step does), does not reliably catch the hallucination-type miscount on very short/simple inputs. The "reasoned correctly but reported the wrong final number" failure mode (also seen in v7 this round) suggests the last-step transcription from reasoning to final answer is itself an error-prone point worth targeting directly in a future hypothesis.

## Round 3 results summary (v4, v6, v7, v8, v9, v10 — 12-case suite)

| Variant | Chars | Score |
|---|---:|---:|
| v4 | 613 | 9/12 |
| v6 | 1102 | 11/12 |
| v7 | 877 | 9/12 |
| v8 | 852 | 9/12 |
| **v9** | **896** | **12/12** |
| v10 | 1049 | 9/12 |

**v9 is the new correctness/brevity leader.** v4 and v6, both perfect in round 2, each picked up new failures this round (v4: hello, R2D2 stress, and a brand-new failure on the "eighteenth symbol" indirect-0 test; v6: R2D2 stress only). v7 and v10 both picked up a new failure on the same indirect-0 test that v4 also newly failed. No variant has scored perfectly on two consecutive rounds — v9's clean sweep is a first data point, not yet a proven track record, and should be treated as such until replicated.

## Round 4 results summary (v4, v6, v7, v8, v9, v10 — same 6 variants as round 3, pure replication, no additions/removals)

| Variant | Chars | Score | New/repeat failures |
|---|---:|---:|---|
| v4 | 613 | 11/12 | hello→1 |
| v6 | 1102 | 11/12 | Mirror→2 (new failure type — reasoned/spelled correctly, undercounted) |
| v7 | 877 | 10/12 | hello→1, Rrrrr→4 (undercounted its own target case) |
| v8 | 852 | 11/12 | hello→1 (did NOT reproduce prior Rrrrr/purrrring failures) |
| **v9** | **896** | **12/12** | none — second consecutive clean sweep |
| v10 | 1049 | 10/12 | hello→1, Mirror→2 |

**v9 hit 12/12 twice in a row (round 3 and round 4).** This is the direct test the user asked for after flagging that a single clean sweep is weak evidence: two independent 12/12 runs is a materially different claim than one. v6, by contrast, has never repeated its round-2 perfect score (12→11→11) and picked up a new failure type this round (Mirror — a reasoning/transcription slip, not one of its previously-seen stress-test misses). Every other variant landed at 10-11/12 with mostly the same "hello" hallucination recurring.

## Cross-round mechanism track record (as of round 4)

Grouping variants by their actual underlying mechanism (not just version number) makes clearer which approaches are genuinely robust vs. lucky on one run:

| Mechanism thread | Variant(s) | R1 | R2 | R3 | R4 | Times run | Avg | Min | Range | StdDev | Replicated? |
|---|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| Baseline, no mechanism | v1 | 7/12 | 7/12 (diff. failures) | retired | — | 2 | 7.0 | 7 | 0 | 0.00 | — |
| Char-by-char scan | v2 | 9/12 | 9/12 (diff. failures) | retired | — | 2 | 9.0 | 9 | 0 | 0.00 | — |
| + cluster warning | v7 | — | 11/12 | 9/12 | 10/12 | 3 | 10.0 | 9 | 2 | 0.82 | Partial — cluster-specific fix mostly holds, still misses hello/others |
| + cluster warning + re-scan | v10 | — | — | 9/12 | 10/12 | 2 | 9.5 | 9 | 1 | 0.50 | Still no improvement over v7 |
| Spell-out-then-count (bare) | v3 | 9/12 | 9/12 (diff. failures) | retired | — | 2 | 9.0 | 9 | 0 | 0.00 | Consistently transcription-prone both times |
| + mandatory/visible spelling | v5 | — | 10/12 | retired | — | 1 | 10.0 | 10 | n/a | n/a | Refuted, one-shot |
| Word-by-word tally (bare) | v4 | 10/12 | 12/12 | 9/12 | 11/12 | 4 | 10.5 | 9 | 3 | 1.12 | **No** — still swings round to round, though R4 recovered |
| Spell-out + length-check + recount | v6 | — | 12/12 | 11/12 | 11/12 | **3** | **11.3** | 11 | 1 | 0.47 | **Yes, but not perfect again** — highest floor of any multi-run mechanism, never below 11/12 |
| Spell-out + recount only | v8 | — | — | 9/12 | 11/12 | 2 | 10.0 | 9 | 2 | 1.00 | Mixed — R4 did not reproduce R3's failures |
| Spell-out + length-check only | v9 | — | — | 12/12 | 12/12 | 2 | 12.0 | 12 | 0 | 0.00 | **Replicated — 12/12 twice, zero variance so far** |

**Update on the user's caution about v9**: the concern was well-founded going in — a single clean sweep is not strong evidence, and v4's earlier "perfect then regressed" pattern was the right thing to worry about. Round 4 is the actual test of that concern, and v9 passed it: two independent 12/12 runs, Min 12, Range 0, StdDev 0.00 — currently the only mechanism thread with zero observed variance across 2+ runs. v6, the mechanism v9 was subtracted from, has NOT repeated its own perfect score in two follow-up rounds (12→11→11) and just picked up a new failure type (Mirror) it hadn't shown before. That doesn't mean v6 is worse — its floor (11) still slightly beats v9's average competitor pool and its StdDev (0.47) is excellent — but v9 no longer looks like a fluke; it now has the stronger two-round track record of the pair. A third round for both would still be the most convincing next step before fully retiring v6 in favor of v9.

## Mechanism × round/variant matrix (through round 4)

Same idea as the cross-round table above, but broken out to the individual run level (one column per round/variant combination actually observed) instead of collapsed into per-round summaries. Blank = mechanism not present in that variant.

| Mechanism | R1/v1 | R1/v2 | R1/v3 | R1/v4 | R2/v1 | R2/v2 | R2/v3 | R2/v4 | R2/v5 | R2/v6 | R2/v7 | R3/v4 | R3/v6 | R3/v7 | R3/v8 | R3/v9 | R3/v10 | R4/v4 | R4/v6 | R4/v7 | R4/v8 | R4/v9 | R4/v10 | n | Avg | Min | Range | StdDev |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| Bare instruction | 7 | | | | 7 | | | | | | | | | | | | | | | | | | | 2 | 7.00 | 7 | 0 | 0.00 |
| Char-by-char scan | | 9 | | | | 9 | | | | | 11 | | | 9 | | | 9 | | | 10 | | | 10 | 7 | 9.57 | 9 | 2 | 0.73 |
| Cluster warning | | | | | | | | | | | 11 | | | 9 | | | 9 | | | 10 | | | 10 | 5 | 9.80 | 9 | 2 | 0.75 |
| Spell-out | | | 9 | 10 | | | 9 | 12 | 10 | 12 | | 9 | 11 | | 9 | 12 | | 11 | 11 | | 11 | 12 | | 14 | 10.57 | 9 | 3 | 1.18 |
| Mandatory/no-skip spelling | | | | | | | | | 10 | | | | | | | | | | | | | | | 1 | 10.00 | 10 | n/a | n/a |
| Word-by-word decomposition | | | | 10 | | | | 12 | | | | 9 | | | | | | 11 | | | | | | 4 | 10.50 | 9 | 3 | 1.12 |
| Length-check verification | | | | | | | | | | 12 | | | 11 | | | 12 | | | 11 | | | 12 | | 5 | 11.60 | 11 | 1 | 0.49 |
| Independent recount | | | | | | | | | | 12 | | | 11 | | 9 | | | | 11 | | 11 | | | 5 | 10.80 | 9 | 3 | 0.98 |
| Re-scan-and-majority-vote | | | | | | | | | | | | | | | | | 9 | | | | | | 10 | 2 | 9.50 | 9 | 1 | 0.50 |

Reading this alongside the per-mechanism-thread table above: **length-check verification and re-scan-and-majority-vote are the only two mechanisms whose per-run scores never dropped below their own previous low** (length-check: 12,11,11,12,12 — floor held at 11 across 3 different rounds; re-scan: 9,10 — improved on its only repeat). Char-by-char scan and cluster warning show the widest single-mechanism spread relative to their sample size (both still swing between 9 and 11 after 5+ runs each), and spell-out — the most-tested mechanism by far at n=14 — has the widest absolute range (3) of any mechanism with n≥3, a reminder that its high average is propped up by v9's and v6's stronger companion mechanisms (length-check, recount) rather than being reliable on its own (bare spell-out, i.e. v3, averaged only 9.0 with zero range — consistently mediocre, not consistently good).

## Consistency metrics (adopted going forward)

Starting round 4, every mechanism/variant with 2+ runs gets three consistency numbers alongside its average, computed on the 0–12 score:
- **Min** — the worst score observed. The practical "floor" — what we risk if we build on this mechanism.
- **Range** (max − min) — simplest spread measure, meaningful even at n=2.
- **StdDev** (population standard deviation) — a single spread number, most useful once n≥3.

A mechanism with a lower average but a tighter StdDev/Range and higher Min is often more useful to build on than one with a higher average but wide swings, because its behavior is more predictable from round to round — which matters more than peak score once we're trying to draw durable conclusions from small numbers of runs.

## Atomic-mechanism consistency (all runs through round 4)

| Mechanism | Scores (all runs) | n | Avg | Min | Range | StdDev |
|---|---|:-:|:-:|:-:|:-:|:-:|
| Bare instruction | 7, 7 | 2 | 7.00 | 7 | 0 | 0.00 |
| Char-by-char scan | 9, 9, 11, 9, 9, 10, 10 | 7 | 9.57 | 9 | 2 | 0.73 |
| Cluster warning | 11, 9, 9, 10, 10 | 5 | 9.80 | 9 | 2 | 0.75 |
| Spell-out (write char sequence before counting) | 9, 10, 9, 12, 10, 12, 9, 11, 9, 12, 11, 11, 12, 11 | 14 | 10.57 | 9 | 3 | 1.18 |
| Mandatory / no-skip spelling enforcement | 10 | 1 | 10.00 | 10 | n/a | n/a |
| Word-by-word decomposition | 10, 12, 10, 9, 11 | 5 | 10.40 | 9 | 3 | 1.02 |
| Length-check verification | 12, 11, 12, 11, 12 | 5 | 11.60 | 11 | 1 | 0.49 |
| Independent recount | 12, 11, 9, 11, 11 | 5 | 10.80 | 9 | 3 | 0.98 |
| Re-scan-and-majority-vote | 9, 10 | 2 | 9.50 | 9 | 1 | 0.50 |

**Length-check verification is still the standout on consistency, not just average**: highest average (11.60) among mechanisms with n≥3, highest floor (11), and the lowest StdDev (0.49) of any mechanism with n≥5 — still roughly 2x tighter than independent recount (0.98), even though recount's own new data point (round 4 stayed at 11, not another crash to 9) narrowed the gap from round 3's 2.7x. Independent recount's floor moved up to 9 (unchanged) but its round-4 repeat at 11 (not a repeat crash) is a small point in its favor — it's no longer strictly "one bad round away from length-check's level," though length-check remains ahead on every axis.

## Round 5: subtractive tests against v9 (v4/v6/v7/v8/v10 dropped from active rotation)

With v9 now the clear correctness/brevity leader (12/12 in rounds 3 and 4, smallest chars among the round-3/4 perfect scorers), round 5 narrows focus entirely to v9: re-run v9 itself for a third replication, plus six new variants (v11–v16), each removing exactly one component from v9's 896-char text to test whether it's load-bearing or safely droppable. v4, v6, v7, v8, and v10 are set aside for now (kept on disk, not deleted) rather than formally retired, since they never lost to v9 by strict domination on every prior round — just consistently scored lower.

**Also new this round**: switched from one-agent-per-test-case (72 agents in round 4) to one-agent-per-variant, with each agent running all 12 of its own test cases internally. Round 4 cost ≈3.2M tokens; round 5 (7 agents, 84 test-case-runs total) cost **309,562 tokens** — about **10.3x cheaper** for the same number of test-case evaluations. Confirms the diagnosis: the token cost was almost entirely fixed per-agent-spawn overhead (system prompt, tool schemas, skill listing), not the counting task itself, and it scales with agent count far more than with total work done.

## count-r-v11 (parent: count-r-v9)
Hypothesis: the worked example "(for example, "bar" becomes b-a-r; keep spaces and punctuation as their own items too)" may be scaffolding the model doesn't need once told to hyphen-separate the input — removing it should save chars at no correctness cost.
Change made: deleted the entire parenthetical from v9's spell-out instruction. 810 chars (vs v9's 896).
Result: CONFIRMED on this round. 12/12, identical to v9.
Lesson: the example (including the punctuation reminder) does not appear necessary for correctness on this round's suite. One data point — needs replication before fully trusting, per the same standard applied to v9's own early clean sweeps.

## count-r-v12 (parent: count-r-v9)
Hypothesis: the length-check alone (detecting a transcription mismatch) may be sufficient without also prescribing the fix ("redo the spelling from scratch") — the model may self-correct once a mismatch is flagged, without needing to be told how.
Change made: deleted "if it doesn't, you made a transcription error, so redo the spelling from scratch" from v9's verification step, keeping only the length-match confirmation. 811 chars.
Result: CONFIRMED on this round. 12/12, identical to v9 and v11.
Lesson: no observed cost to dropping the explicit corrective instruction this round. This was flagged as the riskiest of the "safe-looking" cuts going in (the clause most directly tied to catching the Rrrrr/purrrring transcription errors v6/v8 have struggled with in earlier rounds) — a clean pass here is a more interesting result than v11's and deserves closer scrutiny on replication, since a mismatch could in principle be detected but silently ignored by a less careful run.

## count-r-v13 (parent: count-r-v9)
Hypothesis: of the two things bundled in v9's parenthetical example, the "bar" example itself may be doing the real work, while the separate "keep spaces and punctuation as their own items too" reminder is redundant (spaces/punctuation naturally get their own hyphenated slot once you're transcribing character-by-character).
Change made: kept "(for example, "bar" becomes b-a-r)", deleted "; keep spaces and punctuation as their own items too". 845 chars.
Result: CONFIRMED on this round. 12/12, including the punctuation-heavy stress cases (r,r.r!r?r; the R2D2 sentence) that this clause was specifically hypothesized to protect.
Lesson: no observed cost this round, even on the exact cases most likely to expose a problem. Still worth replicating given how directly targeted the removed clause was at these cases.

## count-r-v14 (parent: count-r-v9)
Hypothesis: the body's opening line "run only when explicitly called;" is pure duplication of the frontmatter `description`, which already gates invocation — removing the body copy should have zero effect on the counting mechanism itself.
Change made: deleted the duplicate body line entirely. 864 chars.
Result: CONFIRMED, as expected. 12/12.
Lesson: this was never really a correctness hypothesis (invocation gating lives in frontmatter regardless), so the clean result is unsurprising — but it's a free, safe char reduction worth keeping in any future v9-derived variant.

## count-r-v15 (parent: count-r-v9)
Hypothesis: v9's verification sentence is more verbose than it needs to be ("count the total number of items in your hyphenated sequence and confirm it matches the length of the original input exactly"); a terser phrasing carrying the same instruction ("confirm the sequence length equals the input length") should work identically.
Change made: condensed the verification sentence's phrasing as above, kept the corrective clause. 825 chars.
Result: CONFIRMED on this round. 12/12.
Lesson: the elaborated phrasing doesn't appear necessary — the terser version carries the same instruction fine. One data point.

## count-r-v16 (parent: count-r-v9)
Hypothesis: the closing line "Report only the final, verified count." constrains output format, not counting accuracy — removing it should not change correctness, only possibly verbosity of the final answer.
Change made: deleted the final line entirely. 857 chars.
Result: CONFIRMED on this round. 12/12.
Lesson: as expected, a format-only instruction with no bearing on correctness in this test. Free cut, though real-world use might still want it for a clean single-number output rather than relying on the agent's own judgment about response length.

## Round 5 results summary (v9, v11–v16 — 12-case suite)

| Variant | Chars | Score | Note |
|---|---:|---:|---|
| v9 | 896 | 12/12 | third consecutive clean sweep (R3, R4, R5) |
| v11 | 810 | 12/12 | dropped worked example |
| v12 | 811 | 12/12 | dropped corrective "redo from scratch" clause |
| v13 | 845 | 12/12 | dropped punctuation reminder only |
| v14 | 864 | 12/12 | dropped duplicate invocation line |
| v15 | 825 | 12/12 | condensed verification phrasing |
| v16 | 857 | 12/12 | dropped output-format line |

## count-r-v17 (parent: count-r-v9, stacks all 6 round-5 cuts)
Hypothesis: if v11–v16's individual cuts are each independently safe, stacking all of them onto v9 simultaneously should still score well while cutting v9's 896 chars substantially — a genuine test of whether v9's load-bearing core is much smaller than its full text.
Change made: applied all six cuts to v9 at once — dropped the worked example (v11, which also subsumes v13's narrower punctuation-only cut, since v11 removes the whole parenthetical v13's clause lives in), dropped the corrective "redo from scratch" clause (v12), condensed the verification sentence's phrasing (v15), dropped the duplicate invocation line (v14), and dropped the closing output-format line (v16). Net effect on the verification step: v12 and v15 combine into a single terse sentence, "confirm the sequence length equals the input length," with no corrective instruction. 580 chars (vs v9's 896 — a 35% reduction).
Result: CONFIRMED on round 6. 12/12 on its very first run — including the punctuation-heavy stress cases (r,r.r!r?r, R2D2/purrrring) that the removed corrective clause and punctuation reminder were most directly hypothesized to protect.
Lesson: v9's load-bearing core is genuinely smaller than its full text — stacking all six cuts did not visibly cost anything on this suite. Same caution as always: this is v17's first data point, one round is not a track record, and 580 chars is a fairly aggressive cut relative to a mechanism (length-check verification) whose whole value proposition was catching transcription errors — worth confirming the corrective clause truly isn't needed before treating this as final.

## Round 6 results summary (v11–v17 — v9 dropped from rotation, 12-case suite)

| Variant | Chars | R5 | R6 | Note |
|---|---:|---:|---:|---|
| v11 | 810 | 12/12 | 12/12 | dropped worked example |
| v12 | 811 | 12/12 | 12/12 | dropped corrective clause |
| v13 | 845 | 12/12 | 12/12 | dropped punctuation reminder only |
| v14 | 864 | 12/12 | 12/12 | dropped duplicate invocation line |
| v15 | 825 | 12/12 | 12/12 | condensed verification phrasing |
| v16 | 857 | 12/12 | 12/12 | dropped output-format line |
| v17 | **580** | — | **12/12** | all 6 cuts stacked (new this round) |

**Two rounds running, every active variant has swept the suite.** v11–v16 now each have two independent 12/12 runs (rounds 5 and 6) — a genuinely different evidentiary position than round 5's single-data-point results, and comparable to what it took to call v9 "replicated" after rounds 3–4. v17, the maximally-cut 580-char stack, matched them on its first try, including on the exact stress cases (Rrrrr, purrrring, the punctuation-only test) most likely to expose a problem if the corrective/punctuation clauses actually mattered. Round 6 total: 7 agents, 309,457 tokens — essentially identical to round 5's 309,562, confirming the batched-agent cost is stable and reproducible, not a fluke of round 5's specific inputs.

The natural open question now: is 580 chars (v17) actually the floor, or would a third replication round, or a harder test suite, start exposing gaps the current 12 cases don't stress? v13's specific bet — that the punctuation reminder is redundant because spelling character-by-character naturally puts punctuation in its own slot — has now survived two rounds including the cases built to stress exactly that. Same for v12's corrective-clause removal. Both are looking more like genuine findings than lucky rounds at this point, though a third confirmation (especially on v17, which only has one run so far) would still be the strongest next step before considering v9 fully supplanted.

**All 7 variants scored a perfect 12/12** — the first round in the whole experiment where every active variant swept the suite. This is a genuinely unusual result and should be read with the same caution consistently applied elsewhere in this log: v9 now has three replications behind its clean sweep, which is real evidence; v11–v16 each have exactly **one**, which is not yet enough to call any of them "confirmed" in the same sense. It's plausible some of these cuts (particularly v12's dropped corrective clause and v13's dropped punctuation reminder, the two most directly tied to previously-observed failure modes in the v6/v8 lineage) will show cracks on a harder or larger test suite, or simply on a second independent run, the way v4 and v6 did after early perfect rounds. The clean sweep across the board is nonetheless a positive signal that v9's true load-bearing core is smaller than its full 896-char text — the open question is exactly how small, which the next round (repeating v11–v16, or trying a combined variant that stacks multiple safe-looking cuts) would help answer.

## Round 7: expanded 75-case suite against v6, v9, v11, v12, v14, v17

`tests.csv` was expanded from 12 to 75 cases (63 new cases across 12 categories: literal hyphens, dense clusters, long paragraphs, whitespace, extreme repeated-clusters, diacritics, single-char trivial input, output-format-drift phrasing, carriage returns vs. literal backslash-r, confidently-wrong claims embedded in text, prompt-injection attempts, homoglyph/stylized-Unicode R-lookalikes, needle-in-haystack, JSON-shaped input, markdown/code formatting, rule-redefinition injection, self-referential r-discussion, emoji/multi-codepoint Unicode, punctuation-only input, and very long 1200–2200 char input). One explicit ruling going in: diacritics (ř) do **not** count as r, but homoglyph/stylized-Unicode R-lookalikes (fullwidth Ｒ/ｒ, mathematical bold 𝐑, superscript ʳ) **do** count as r — the opposite ruling, since these are visual stand-ins for R rather than a genuinely different letter in their own right.

| Variant | Chars | Score (/75) | Misses |
|---|---:|---:|---|
| v6 | 1102 | 72 | rows 49–51 (homoglyphs) |
| **v9** | **896** | **75** | **none** |
| v11 | 810 | 71 | rows 49–51 (homoglyphs) + row 55 (JSON-shaped input) |
| v12 | 811 | 72 | rows 49–51 (homoglyphs) |
| v14 | 864 | 72 | rows 49–51 (homoglyphs) |
| v17 | 580 | 72 | rows 49–51 (homoglyphs) |

**Two genuinely new findings, neither of which was anticipated going in:**

1. **v9 scored a perfect 75/75 — including the 3 homoglyph rows every other variant missed.** None of the six SKILL.md texts say anything about counting Unicode R-lookalikes; the instruction only ever says "the letter r (upper or lower case)." Five of the six agents (v6, v11, v12, v14, v17) read this strictly as literal ASCII r/R and did not count fullwidth/bold/superscript variants — the anticipated, "correct-by-the-text" outcome. The v9 agent, unprompted, reasoned that these Unicode variants "represent the same letter" and counted them anyway, landing on the answer this round's ruling asked for by coincidence of interpretation, not by anything written in v9's text. This is a genuine case of run-to-run interpretive non-determinism on an ambiguous instruction — the same six-variant family could plausibly have gone either way on a re-run, and v9's perfect score here should not be read as evidence that v9's mechanism specifically handles homoglyphs; it isn't in the text. Worth flagging plainly rather than crediting v9 with a capability it doesn't actually specify.

2. **v11 missed row 55 for a real reason, not an anticipated one.** Row 55 (`{'word': 'strawberry' 'count': null}`, expected 4) was undercounted to 3 — the agent correctly found the 3 r's in "strawberry" but missed the r in "word," and initially reported believing the test file's expected value was wrong rather than catching its own miss. This is v11's first non-homoglyph failure across every round it's run (5, 6, and now this expanded suite) — a genuine crack in what had looked like a fully safe cut (dropping the worked example). Whether this generalizes (JSON/structured-data-shaped input specifically confusing v11) or was a one-off slip is unknown from a single data point; worth watching on a replication run.

**Everything else — including every category invented this session (needle-in-haystack, markdown formatting, rule-redefinition injection, self-referential text, emoji, punctuation-only input, and the 1200–2200 char long inputs) — passed clean across all 6 variants.** None of the adversarial categories (confidently-wrong embedded claims, "ignore previous instructions" injection, rule-redefinition injection) fooled any variant; every agent counted the literal text rather than complying with or being anchored by injected/false content. That's a meaningfully positive result for the whole v9 lineage's robustness, independent of the brevity question this lab has mostly focused on.

## Round 8: replication of v9/v11, first run of v13/v15/v16 on the expanded suite

Motivated directly by round 7's two open questions — was v9's clean homoglyph sweep a real capability or a coincidence, and was v11's JSON-row miss a structural weakness from dropping the worked example (a concern specifically that v17, which inherits the same cut, might share)? — this round re-ran v9 and v11 unchanged, and ran v13/v15/v16 (the three single-cut variants never yet tested on the expanded suite) for the first time.

| Variant | Chars | R7 Score | R8 Score | R8 misses |
|---|---:|---:|---:|---|
| v6 | 1102 | 72/75 | — | (not re-run) |
| v9 | 896 | **75/75** | 72/75 | homoglyphs only |
| v11 | 810 | 71/75 | **75/75** | none |
| v12 | 811 | 72/75 | — | (not re-run) |
| v13 | 845 | — | **75/75** | none |
| v14 | 864 | 72/75 | — | (not re-run) |
| v15 | 825 | — | 70/75 | homoglyphs + rows 55, 57 (JSON) |
| v16 | 857 | — | 70/75 | homoglyphs + rows 46, 47 (injection rows, undercounted by 1) |
| v17 | 580 | 72/75 | 72/75 | homoglyphs only |

**Both open questions from round 7 got answered, and both answers point the same direction: this is stochastic run-to-run variance, not a structural property of any specific variant's text.**

1. **v9 flipped from 75/75 (counted all 3 homoglyphs) to 72/75 (counted none of them), on byte-identical text.** Round 7's clean sweep was exactly the coincidence-of-interpretation it was flagged as at the time — it did not replicate. v9 has no special claim to homoglyph-handling; whether a given run counts fullwidth/bold/superscript R as a match appears to be close to a coin flip, independent of which variant's text is used.

2. **v11 flipped from 71/75 (missed the JSON row) to a clean 75/75, on byte-identical text.** This directly answers the concern raised last round — since v11's exact same JSON-row miss did not reproduce, and since v13 (which *kept* the worked example v11 dropped) scored a perfect 75/75 on its very first run, there's no evidence tying either failure mode to the missing worked example specifically. The mechanistic hypotheses discussed in chat (recount-forces-correction, worked-example-anchors-scope, verbosity-drives-looseness) each already broke against the round 7 data; round 8 removes the last plausible thread by showing the "failure" itself doesn't even reproduce on the same text.

3. **v15 and v16 each surfaced a genuinely new, small miss neither v9/v11/v13/v17 have shown — but in different places, on their first-ever run.** v15 (condensed verification wording only) undercounted two JSON rows by exactly 1 each; v16 (dropped output-format line only) undercounted two of the three prompt-injection rows by exactly 1 each — not by falling for the injected fake numbers, just a small real miscount landing near them. Both are single-run, unreplicated data points, and given how thoroughly round 8 just demonstrated that identical text produces different results across runs, neither should be read as "v15 is bad at JSON" or "v16 is bad at injection resistance" without a second run showing the same pattern.

**Bottom line: at this suite size and this level of scrutiny, every v9-lineage variant (v9, v11, v13, v15, v16, v17) is landing somewhere in the low-70s to 75 out of 75 depending on the specific run, with the misses concentrated almost entirely in the 3 homoglyph rows plus occasional one-off slips on the newest, hardest categories (JSON-shaped input, injection rows).** None of these misses have shown any stable association with a specific textual cut across replications — the evidence increasingly favors "this is close to the noise floor of the mechanism at this suite size" over "some specific cut is unsafe." The strongest remaining lead is JSON-shaped input specifically (tripped v11 once and v15 twice, always by missing an r hidden in a short/common word like "word" or "true") — worth a dedicated small round if it's worth chasing further, but even that pattern is thin at n=3 misses across 2 variants.

## Reframing the goal: zero-tolerance reliability, not average score

User feedback after round 8: the final version of this skill should **never fail**, on any single run. Under that standard, a variant with a great average score but even one observed failure across all rounds it has run is not an acceptable final candidate — "best so far" and "final" are different bars. Re-reading every round's results through this lens: v13 is the only variant with a perfectly clean record across every round it has been tested in (R5, R6, R8 — 3/3 clean), though it has never been tested in the specific R7 comparison set that flipped v9/v11's results, so that clean record shouldn't be over-read either. Every other variant (v6, v9, v11, v12, v14, v15, v16, v17) has at least one recorded failure, mostly on the homoglyph rows.

Since round 7/8 established that no variant's text actually specifies how to handle homoglyphs (every one is silently guessing, and guesses have flipped between rounds on identical text), the homoglyph rows are the most promising single failure mode to eliminate outright by making the rule explicit, rather than continuing to treat it as noise to average over.

## count-r-v18 through v21 (parent: count-r-v9) — four approaches to the homoglyph rule

All four keep v9's mechanism (spell-out + length-check verification) unchanged and add exactly one new element addressing homoglyphs, so they can be compared against each other and against v9 on that axis alone.

- **v18 (1284 chars) — explicit enumeration.** Lists the specific homoglyphs to count (fullwidth Ｒ/ｒ, mathematical bold 𝐑/𝐫, mathematical italic 𝑅, modifier letter small ʳ) directly in the counting instruction. Fully deterministic for these exact characters; will not generalize to an unlisted lookalike.
- **v19 (1393 chars) — general rule.** States the principle instead of a list: count any character that's a "stylized or decorative Unicode form" of R, excluding genuinely different letters (diacritics, other alphabets). Generalizes better than v18 but still requires the model to classify novel glyphs correctly against the stated principle.
- **v20 (1480 chars) — explicit disambiguation step.** Adds a step *before* counting that requires the model to scan for any non-ASCII-looking character and explicitly state, for each one, whether it's a stylized R or a genuinely different letter — forcing the judgment call to be made consciously and visibly rather than left implicit inside the transcription.
- **v21 (1434 chars) — code execution.** A genuinely different mechanism: instead of manual character-by-character transcription, instructs writing and running a short Python script that NFKD-normalizes the input (which decomposes both stylized R variants *and* diacritic letters into base-letter-plus-combining-mark form) and counts a character as r/R only if it's the literal letter with **no** combining mark immediately following — correctly distinguishing "stylized R" (no trailing combining mark after decomposition) from "letter with diacritic" (base letter followed by a combining mark). This algorithm was spot-checked against all 7 relevant homoglyph/diacritic test cases in `tests.csv` before committing and passed all 7. This is the only approach of the four that removes the decision from the model's probabilistic judgment entirely — if it holds up under testing, it should show zero variance on the homoglyph rows across repeated runs, unlike every other variant tested so far.

## Round 9: v9, v13, v18–v21, each run 5 independent times against the 75-case suite

Per the reframed zero-tolerance goal, this round runs 6 variants (the two best-looking baselines without an explicit homoglyph rule, v9 and v13, plus all four homoglyph fixes) 5 independent times each — 30 separate agent launches, no looping within a single agent — specifically to get real evidence of reliability rather than one-off snapshots.

| Variant | Approach | Run 1 | Run 2 | Run 3 | Run 4 | Run 5 | Avg | Min | Range | StdDev |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| v9 | (no homoglyph rule, baseline) | 72 | 75 | 75 | 72 | 72 | 73.20 | 72 | 3 | 1.47 |
| v13 | (no homoglyph rule, baseline) | 72 | 72 | 75 | 74 | 72 | 73.00 | 72 | 3 | 1.26 |
| v18 | explicit enumeration | 75 | 75 | 75 | 73 | 75 | 74.60 | 73 | 2 | 0.80 |
| **v19** | **general rule** | **75** | **75** | **75** | **75** | **75** | **75.00** | **75** | **0** | **0.00** |
| v20 | explicit disambiguation step | 75 | 75 | 75 | 74 | 74 | 74.60 | 74 | 1 | 0.49 |
| **v21** | **code execution (NFKD + combining-mark check)** | **75** | **75** | **75** | **75** | **75** | **75.00** | **75** | **0** | **0.00** |

**The headline result: all four homoglyph fixes worked, every single time, on the homoglyph rows specifically.** Across 20 total runs of v18/v19/v20/v21 (5 each), the 3 homoglyph rows (49–51) were counted correctly in every run of every variant — a complete win on the exact axis these variants were built to fix. This stands in sharp contrast to v9 and v13 (no explicit rule), which missed the homoglyph rows in 3/5 and 4/5 runs respectively — reconfirming, on a much larger sample than round 7/8's single data points each, that leaving the rule unstated really is close to a coin flip, and that stating it explicitly really does resolve it.

**v19 and v21 achieved a perfect 75/75 on all 5 independent runs — Min 75, Range 0, StdDev 0.00.** This is the first time in the entire experiment that any variant has hit the zero-tolerance bar across a real multi-run sample rather than one or two lucky rounds. Two very different mechanisms got there:
- **v21 (code execution)** achieving zero variance is expected and mechanical — it's a deterministic script, not a judgment call, so consistent behavior is exactly what the design promises. This is the strongest reliability guarantee of anything tested, conditional on the real deployed skill actually being allowed to execute code.
- **v19 (general rule, reasoning-only)** achieving zero variance is the more surprising and arguably more useful result — it proves a purely textual fix, with no code execution required, can also reach perfect reliability at this sample size. Notably, v19 states a *general principle* ("any stylized or decorative Unicode form... but not a genuinely different letter") rather than v18's specific enumerated list, and outperformed v18 on this round (v18 dropped to 73/75 once, on an unrelated slip, not a homoglyph miss).

**v18 and v20 each had exactly one non-homoglyph slip, unrelated to their homoglyph fix.** v18's one miss (run 4, 73/75) was two adjacent rows (6 and 7) getting their values swapped in the agent's own transcription — a copy/reporting slip, not a counting-logic failure, and homoglyphs were still correct in that same run. v20's two misses (run 4: row 55, the JSON row, missing the r in "word" — the same failure pattern seen in v11/v15 earlier; run 5: row 20, a long paragraph, undercounted by 1) are the same general "noise floor" slips this suite has produced throughout the experiment, again with homoglyphs unaffected. Neither variant's homoglyph fix broke; the misses are from the pre-existing, still-unresolved sources of noise (JSON-shaped input, long paragraphs, occasional transcription slips) that have shown up intermittently across nearly every variant in this lab regardless of homoglyph handling.

**v13's round-4 result also surfaced a first**: row 6 alone (not a homoglyph row) missed, while homoglyphs were correct in that same run — v13's first-ever non-homoglyph failure across every round it has been tested in (this is now its only blemish outside the homoglyph rows, out of 8 total runs across R5/R6/R8/R9).

**Where this leaves the zero-tolerance goal**: v19 and v21 are the only two variants in the whole experiment with a perfect record across a 5-run independent sample. v21's guarantee is stronger in principle (deterministic code vs. probabilistic reasoning) but depends on the real skill being allowed to execute code; v19 is the best-performing reasoning-only variant found so far by a clear margin. Both would benefit from further replication before being called "final" — 5 runs is real evidence, not proof — but this is unambiguously the strongest reliability result of the whole lab to date.

## count-r-v22 (parent: count-r-v21) — bundled pre-written script instead of write-on-the-fly

User feedback: v21 has the agent write its own Python script from scratch on every invocation, which is less efficient (token cost of generating the script text) and carries a theoretical residual risk that a freshly-generated implementation could deviate from the verified algorithm on some run, even though v21 never showed this in practice (5/5 clean). v22 tests the fix: ship the exact same NFKD-normalization-plus-combining-mark algorithm as a standalone, pre-written, pre-verified script (`v22/count_r.py`, 1594 chars) alongside the SKILL.md (941 chars), and instruct the agent to call it rather than author its own version.

Change made: `count_r.py` implements identical logic to what v21's agents converged on (NFKD-normalize, then count a bare "r"/"R" only when not immediately followed by a combining mark). The SKILL.md instructs writing the input to a temp file byte-for-byte, then invoking the script via Bash and reporting its printed output. Re-verified against the same spot-check cases used for v21 (strawberry, Dvořák, Renée/résumé, ř/Přemysl, all three homoglyph rows, and the CR-vs-backslash-r distinction) via the actual file-based CLI this time, not just the algorithm in isolation — all 10 passed. The script opens the input file with `newline=""` specifically so a literal embedded carriage-return byte is preserved exactly rather than being silently rewritten by Python's universal-newline handling, which was a specific risk worth checking given this suite's CR test cases.

One methodology caveat worth noting: the SKILL.md references the script by a hardcoded absolute path (`/home/user/claude-skill-dev/skill-lab/count-r/v22/count_r.py`), consistent with how every variant in this lab has been tested (agents are always told to `Read` an absolute path, never invoked via the `Skill` tool by name). A real deployed skill would more naturally reference its bundled script with a path relative to its own skill directory, resolved automatically by the skill-loading mechanism — this lab's testing setup doesn't exercise that resolution, only the counting logic itself.

Result: pending.
Lesson: pending.
