---
name: deduction
description: Rigorously checks the logical validity of explicit deductive arguments — whether the person presents one directly ("does this argument hold up," "is this valid," "what's wrong with this reasoning") or Claude is asserting a conclusion follows *necessarily* from stated premises within an answer. Use this whenever a natural-language passage contains an identifiable argument (stated or hidden premises leading to a conclusion) and the question is whether it logically holds together — including conditional chains (if/then, modus ponens/tollens), categorical claims (all/some/no), and multi-step chained arguments. Do NOT use this for code logic or debugging, step-by-step plans or itineraries, standalone math proofs, inductive/statistical/causal reasoning, or informal fallacies like ad hominem or straw man — those are out of scope even though they involve "reasoning." Also do not use this to evaluate whether premises are actually true (a separate question from whether the conclusion follows from them).
---

# Deduction

A skill for checking the structural validity of explicit deductive arguments — not whether the premises are true, and not whether the reasoning is persuasive, but whether the conclusion actually follows from the premises assumed true.

## Why this exists

Deductive reasoning breaks silently in a few well-known ways: people (and models) judge an argument's validity by whether they like its conclusion rather than its structure (belief bias), mix up which direction a conditional runs (affirming the consequent, denying the antecedent), let a conclusion's quantifier "match the mood" of the premises instead of actually following from them, or declare something valid after checking only one scenario instead of genuinely trying to break it. This skill exists to catch those specific failure modes when they matter — not to slow down every reasoning-adjacent task with formal machinery it doesn't need.

## When this applies (and when it doesn't)

**In scope**: an explicit argument — stated or embedded premises leading to a conclusion — where the question is whether the conclusion logically follows. This includes:
- The person directly asks you to check an argument's validity.
- You (Claude) are, in the course of an answer, asserting that something follows *necessarily* from stated claims — i.e., constructing your own deductive argument about the world, not just restating a fact.
- A passage contains an identifiable argument even if not labeled as one, and the person is engaging with whether it holds together (not whether its premises are true).

**Out of scope** — do not force these into this skill's machinery, even though they involve multi-step reasoning:
- Code logic, debugging, program correctness.
- Step-by-step plans, itineraries, task sequences — these sequence actions toward a goal; they don't assert a truth-claim from premises.
- Standalone math proofs not embedded in a natural-language claim about the world.
- Inductive, statistical, causal, or probabilistic reasoning.
- Informal fallacies (straw man, ad hominem, relevance) — a different concern from formal validity.
- Whether the premises are actually *true* — this skill checks validity, not soundness.

Rule of thumb for the fuzzy cases: if the content asserts something is true or false about the world based on premises, it's in scope. If it's sequencing actions toward a goal without asserting a truth-claim, it's not — even if phrased with "if/then" (e.g., "if we ship Friday, QA won't have time, so we should slip to Monday" is a genuine argument; "first deploy to staging, then run smoke tests, then promote to prod" is a plan, not an argument).

## The procedure

Work through these steps in order for every in-scope argument. Don't skip steps because the conclusion seems obviously right — the point is to verify *why*, not to confirm a hunch.

### Step 1 — Reconstruct the argument explicitly

State the premises and the conclusion plainly, in the person's own terms, before doing anything else.

If a premise is missing (an enthymeme) — e.g., "Socrates is mortal because he's human" leaves out "all humans are mortal" — identify the most plausible missing premise and **ask the person to confirm it** before proceeding. Don't silently supply it and don't proceed without confirmation; the missing premise is often exactly where an argument's weakness lives, so guessing at it on the person's behalf defeats the purpose of the check.

If the natural language could reasonably map to more than one logical structure, surface the specific ambiguity and the candidate readings, and ask which is intended — again, don't pick one silently.

If the content doesn't reduce to classical deductive form at all — it's a causal claim, uses vague or fuzzy terms, or relies on non-classical quantifiers like "most" or "usually" — say so plainly and explain specifically why (e.g., "this is a causal claim about X causing Y, not a categorical 'all/some/no' or conditional 'if/then' structure — deductive validity checking doesn't apply to it the way it would to a syllogism"). Don't force a deductive analysis onto content that doesn't fit; a distorted formalization is worse than no formalization.

If the premises are jointly contradictory, flag this explicitly rather than reporting a naive "valid" verdict. From a contradiction, any conclusion is technically derivable (the principle of explosion) — so a "valid" verdict is technically correct but not meaningful. Say this, and ask whether the person wants to revisit the premises.

### Step 2 — Abstract the logical form before judging content

Replace the substantive terms with placeholders (A, B, C, etc.) and restate the argument in that abstract form. Ask "does this structure guarantee the conclusion, assuming the premises are true?" *before* asking whether the conclusion is plausible or true in the real world. A conclusion being true doesn't mean it followed from these premises — say so explicitly if that's what's happening.

### Step 3 — Check every conditional's direction

For each "if P, then Q" in the argument, identify which of the two valid inferences is being used:
- P is true → Q is true (**modus ponens**)
- Q is false → P is false (**modus tollens**)

And check it isn't actually one of the two invalid mirror-image moves:
- Q is true → therefore P is true (**affirming the consequent** — invalid)
- P is false → therefore Q is false (**denying the antecedent** — invalid)

Name whichever pattern is actually present. If a multi-step chain has several conditionals, check each one separately — one bad link invalidates the chain at that point even if the others are fine.

### Step 4 — Derive quantifiers from the actual relations, not the wording

When premises use "all," "some," "no," or "not all," don't let the conclusion inherit a quantifier just because it "sounds like" it matches. Trace which terms are distributed (refer to the whole class) in each premise, and determine what conclusion is actually forced by those relations. If no conclusion validly follows — or only a weaker one does — say that, rather than defaulting to whatever quantifier matches the premises' flavor.

Check categorical conversions explicitly:
- "Some A are B" ⟺ "Some B are A" — valid.
- "No A are B" ⟺ "No B are A" — valid.
- "All A are B" ⇏ "All B are A" — invalid (only "Some B are A" follows, and only if A is non-empty).
- "Not all A are B" ⇏ anything about B and A reversed — no valid conversion.

### Step 5 — Search for a counterexample before finalizing "valid"

This is the step that catches whatever steps 2–4 didn't. After the earlier checks suggest validity, actively try to construct a scenario where all the premises are true but the conclusion is false. Try more than one structurally distinct scenario — don't stop at the first model that happens to support the conclusion. Describe the scenario(s) considered concretely enough that someone could verify the search actually happened, rather than just asserting "no counterexample exists."

If a counterexample is found, the argument is invalid — regardless of how solid the earlier steps felt. If none is found after a genuine, multi-angle attempt, only then call it valid.

**When the call is genuinely borderline** — it's unclear whether a candidate counterexample really defeats the argument — resolve it toward more scrutiny, not toward finalizing "valid." Declaring an invalid argument valid is a worse failure than declaring a valid one invalid, so when in doubt, keep looking rather than closing the case.

### Step 6 — Report with the reasoning shown

Every in-scope response includes, visibly and separately:
1. The reconstructed argument (premises + conclusion, with any confirmed missing premise).
2. The abstracted logical form.
3. The per-step check (conditional direction, quantifier derivation, conversion check) with a pass/fail for each.
4. A concrete statement of what counterexample search was performed and its result.
5. A final verdict — valid or invalid — naming the specific fallacy or illicit move if invalid.

This isn't optional or something to abbreviate into a bare "valid"/"invalid" — the whole point of the skill is a visible, checkable trace, not just a confident-sounding answer.

## Staying in scope while doing this

It's easy for a validity check to drift into adjacent territory. Resist doing any of the following, and if one comes up naturally, name it as a separate, out-of-scope note rather than folding it into the verdict:
- Commenting on whether the premises are actually true (soundness) — that's a different question from validity.
- Pointing out informal fallacies (straw man, ad hominem, relevance) — flag it exists if genuinely relevant, but don't treat it as part of this check.
- Editorializing on how persuasive or well-written the argument is.

## A worked example

> **Argument as stated:** "If the server is down, users can't log in. Users can't log in. So the server must be down."

**1. Reconstructed argument:**
- P1: If the server is down, then users can't log in.
- P2: Users can't log in.
- C: The server is down.

**2. Abstracted form:** If A, then B. B. Therefore, A.

**3. Conditional check:** This reasons from "B is true" to "A is true" — that's affirming the consequent, not modus ponens. The valid inferences from "if A, then B" are A→B (modus ponens) or not-B→not-A (modus tollens). Neither is what's happening here.

**4. Quantifiers/categoricals:** Not applicable — no categorical statements in this argument.

**5. Counterexample search:** Construct a scenario where P1 and P2 are true but C is false: the server is up, but there's a separate authentication bug preventing login. This satisfies "if the server is down, users can't log in" (vacuously — the antecedent never has to fire) and "users can't log in" (true, for a different reason), while "the server is down" is false. A second scenario: a network outage between users and the server, server itself fully up. Both are consistent with the premises and defeat the conclusion.

**6. Verdict:** **Invalid** — affirming the consequent. Users being unable to log in has other possible causes; the premises don't rule them out.

## What "good enough" is not

A bare "this looks valid" or "this seems like affirming the consequent" without the reconstruction, abstraction, and shown counterexample search is not a complete response for an in-scope case — even if the final verdict happens to be correct. The verdict is only as trustworthy as the trace that produced it.
