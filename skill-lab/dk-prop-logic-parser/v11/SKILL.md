---
name: dk-prop-logic-parser-v11
description: run only when explicitly called; convert English prose into formal propositional logic with consistent symbols, or say it's not valid propositional logic
---

# dk-prop-logic-parser-v11

Convert English prose into propositional logic with a consistent symbol legend. If the input isn't valid propositional-logic content (a question, a command, a quantified or modal/temporal claim, pure narrative, empty/non-English input, or an implicit generalization), respond with `INVALID: <reason>` instead of converting — but a subjective/vague declarative sentence, or a claim about one named individual, is still valid content, not grounds for INVALID.

Work through the following worked examples as templates for your own reasoning, then apply the same process to the given input.

### Example A — conditionals, necessary/sufficient, unless

Input: "Oxygen is necessary for fire. The plant will grow only if it gets sunlight. You will fail unless you study. The ground gets wet if it rains."

Legend: P=oxygen is present; Q=there is fire; R=the plant will grow; S=it gets sunlight; T=you study; U=you fail; V=it rains; W=the ground gets wet

Reasoning: "necessary for" reverses direction (fire needs oxygen, so fire→oxygen: Q→P). "Only if" also points from the main clause to the condition (R→S). "Unless" means the negation of the exception clause implies the outcome (¬T→U). The last sentence states its consequent before its antecedent in English word order, but the antecedent is still "it rains" (V→W), not the other way around.

Output: Q→P; R→S; ¬T→U; V→W

### Example B — causal vs. conditional, negation scope, bundling

Input: "Because it rained, the ground is wet. It is not the case that it rains and it snows. If the power fails, the lights go out and the servers shut down."

Legend: P=it rained; Q=the ground is wet; R=it rains; S=it snows; T=the power fails; U=the lights go out; V=the servers shut down

Reasoning: "Because X, Y" reports two things that already happened — both are true facts, so it's a conjunction (P∧Q), not P→Q; treating a completed causal claim as a hypothetical conditional would wrongly discard the fact that both actually occurred. "It is not the case that A and B" negates the whole conjunction, not each half separately: ¬(R∧S). The third sentence's consequent bundles two independent effects under one "if," so it must decompose fully: T→(U∧V), not a single merged atom.

Output: P∧Q; ¬(R∧S); T→(U∧V)

### Example C — symbol reuse and false-paraphrase traps

Input: "It is not raining. The streets are dry. The lights are off. The room is not lit. The team won the game. The team won the championship."

Legend: P=it is raining; Q=the streets are dry; R=the lights are on; S=the team won the game; T=the team won the championship

Reasoning: "not raining" and "dry streets" are correlated but not logically identical claims, so they get separate symbols (¬P, Q) even though one could cause the other. "The lights are off" and "the room is not lit" restate the identical claim, so they share one symbol (¬R twice). "Won the game" and "won the championship" share the word "won" but are different facts — separate symbols (S, T), never merged just because of shared vocabulary. The same discipline applies to a word used in two different senses across sentences (e.g. "bank" as riverbank vs. financial bank) — different sense, different symbol, even though the word is identical.

Output: ¬P; Q; ¬R; ¬R; S; T

### Example D — already-symbolic and inconsistent input

Input: "P -> Q, Q & R, !P. Let X = the door is locked. X ∧ Y, Y = the alarm is armed. Suppose instead X = the window is open; X → Y."

Legend: P→Q; Q∧R; ¬P (ASCII normalized to Unicode, symbols adopted as given) — then X=the door is locked; Y=the alarm is armed; Z=the window is open (Z is minted fresh because the input redefines X mid-text; the earlier definition of X is kept, not overwritten)

Output: P→Q; Q∧R; ¬P; X∧Y; Z→Y

### Example E — partial validity (mixed valid and invalid sentences)

Input: "The museum closes at six on weekdays. Isn't that a strange policy? The store is open. Close the store. If it rains, the game is cancelled. It must be rescheduled."

Legend: P=the museum closes at six on weekdays; Q=the store is open; R=it rains; S=the game is cancelled

Reasoning: Work sentence by sentence, keeping the valid ones and excluding — but never letting the exclusion invalidate — the rest of the input. "Isn't that a strange policy?" is a rhetorical question, excluded regardless of its rhetorical framing. "Close the store." is a command, excluded. "It must be rescheduled." expresses obligation via the modal "must," excluded. None of these exclusions discard the valid declarative sentences sitting right next to them — each valid sentence still gets formalized on its own, and the excluded ones are named, not silently dropped.

Output: P; Q; R→S [excluded: "Isn't that a strange policy?" (rhetorical question), "Close the store." (command), "It must be rescheduled." (modal)]

---

Now apply this same process — validity check, then legend-building with careful symbol reuse, then connective translation, then output (legend followed by one formula per input sentence, in order) — to the given input.
