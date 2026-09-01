# Deferred design ideas — repo-wide

A backlog for meta-level design ideas surfaced during work on this repo's skill labs, judged worth pursuing eventually but deliberately not built immediately — usually because building the structure now would mean designing it from too few real examples (the same mistake `HYPOTHESIS-PRINCIPLES.md`'s tracking table made once already: don't build the framework before there's real data to design it against). Log the idea and the reasoning for deferring it; don't let it decay from memory just because it isn't active work yet.

This is intentionally outside `skill-variant-lab/SKILL.md`'s Standing disciplines/Hard rules/Steps — it isn't a decided rule, and putting it there would both misrepresent its status and trigger that file's audit-gate for no reason.

## Scope-levels-of-learning framework

**Logged:** 2026-09-01, during work on `dk-prop-logic-parser`'s Round 4 close-out and the `lesson-auditor` audit-gate mechanism.

**The idea:** this repo has accumulated several different places a "lesson" can live, at different implicit scopes, but nothing names those scopes explicitly or gives a process for deciding which one a new lesson belongs at. Worth eventually designing: an explicit ladder of scope levels, plus criteria for placing a given lesson at the right one (and promoting it upward when evidence shows it belongs higher).

**What's already observable, as seed material for that design** (not a finished taxonomy — just what's visibly in use today):
- A raw realization in conversation, never written anywhere — decays, scope: nothing.
- A project-specific `## Process note` in one project's `HYPOTHESES.md` — scope: that lab only.
- A cross-project process lesson, meant to be promoted into `skill-variant-lab/SKILL.md`'s Standing disciplines/Hard rules/Steps (Step 13 already names this promotion criterion, but nothing currently checks whether it's actually followed) — scope: every future lab.
- A narrower cross-lab lesson specifically about how to *write variant text* (`skills/skill-variant-lab/references/text-principles.md`) — cross-lab but domain-narrow, a different shape than the process-level tier above it.
- A lesson specifically about how to *generate and value hypotheses* (`skill-lab/HYPOTHESIS-PRINCIPLES.md`, principle-tagged, IV/AV-scored) — another domain-narrow cross-lab tier.
- A lesson about how to *audit other lessons* (`.claude/agents/lesson-auditor.md` itself) — meta-level, one layer above all of the above.
- A lesson that isn't about `skill-variant-lab` at all, but about how to operate in this harness generally (e.g. a live example hit this same day: don't mutate files via `git stash` while a background audit agent may still be reading them) — doesn't obviously belong anywhere in this repo's current structure.

**Why deferred rather than designed now:** only one clear example (the promotion-check idea below) has actually come up organically so far. Designing a general framework from one data point risks the same failure as building `HYPOTHESIS-PRINCIPLES.md`'s tracking table before any hypothesis had actually been generated principle-first — a plausible-looking structure with no real cases to check it against. Better to let a few more "which level does this belong at" moments occur naturally and design from those.

**Trigger to revisit:** the next time a lesson's correct scope-level is genuinely unclear or disputed, or once `lesson-auditor`'s promotion-check (see below) has surfaced a few real un-promoted-lesson cases to design against.

## Related, smaller, not-yet-built item: lesson-auditor promotion-check

Separate from the framework above, but the concrete case that prompted it: add a check to `.claude/agents/lesson-auditor.md`'s Step 2 verifying that Process notes meeting Step 13's promotion criterion ("points at a gap in skill-variant-lab itself, not just a one-off mistake in this particular lab") have actually been promoted into `skill-variant-lab/SKILL.md`, rather than sitting un-promoted indefinitely. This is well-scoped and doesn't need the larger framework above to be built first — status as of this note: proposed in conversation, not yet implemented.
