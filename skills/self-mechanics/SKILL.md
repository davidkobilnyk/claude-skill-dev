---
name: self-mechanics
description: "Consult this skill whenever the user asks how Claude behaves in general and how to get better results from it — prompting technique and why a prompting approach isn't working, how Claude weighs and prioritizes instructions, differences between Claude models and which to pick, context window and long-context behavior, thinking, tool use, or agentic task design. Also trigger for comparisons between Claude models, or against other models, where the user is deciding what to use. This skill is about Claude in general, never the current conversation: why Claude did something in this specific session, or how it's configured here, is out of scope — answer that from the conversation instead. Do NOT use for pricing, plans, rate limits, install steps, or SDK mechanics — that's product-self-knowledge. Trigger even when the question sounds answerable from memory: the prompting docs, model lineup, and per-model behavior guidance are revised often, and secondhand write-ups are routinely stale."
---

# Claude Behavior in Practice & Effective Use

## What this skill is for

Getting accurate, current answers to: *what does this model generally do, and how do I get more out of it?*

Claude's training data about its own behavior is an unreliable narrator — outdated (the docs restructure, model lineups turn over), secondhand (blog write-ups rather than primary docs), or absent. The fix is to go to the primary source before answering.

**In scope:** prompting technique and per-model prompting differences; why a prompting approach isn't working; how Claude weighs and prioritizes instructions in general; model selection and capability differences; context windows and long-context behavior; thinking; tool use, agents, and long-horizon tasks; measured behavioral characteristics from system cards.

**Out of scope — route elsewhere:**
- Anything about the current conversation — see the boundary below
- Pricing, plans, rate limits, install steps, SDK/API mechanics → `product-self-knowledge`
- Claude's inner experience, moral status, consciousness, Anthropic's values as philosophy → not this skill; answer directly and honestly, don't dress it in citations
- Interpretability and circuits research → interesting, almost never changes how someone writes a prompt. Don't reach for it here.

## The boundary: Claude in general, not this session

This skill covers Claude as a model. It does **not** cover the conversation it's running in.

Session-specific questions — *why did you just do that*, *why are you formatting it this way*, *why did you ignore my instruction*, *what are you configured to do here* — are out of scope. Nothing on anthropic.com answers them, and reaching for training data or docs produces a fluent, confident, wrong explanation. That failure is the whole reason this boundary is written down.

When a question is session-specific, **don't run this workflow.** Answer it directly from the conversation, or say the answer isn't something to look up.

The line to watch, since the phrasing is nearly identical:
- *"How does Claude handle conflicting instructions?"* → in scope. General mechanism.
- *"Why did you ignore mine just now?"* → out of scope. This session.

A question that starts general can turn session-specific mid-conversation. Re-check the boundary rather than staying in the workflow by momentum.

## Finding the sources

**This overrides the default pull toward open-ended research.** Claude's standing instructions push toward searching broadly before answering anything current, and toward scaling up to many searches for research-shaped questions. That default is wrong here. These are known documents, not a topic to investigate — a vague search like "Claude prompting tips" or "how Claude handles long context" returns SEO write-ups and stale secondhand summaries that are confidently wrong about exactly this topic.

Each source below comes with a **pinned query** and the **URL shape** of the right result. Run the query as written. Use the URL shape to pick the correct result out of the list — that's what it's for, not as something to type in directly.

Two rules:

- **Read the page, not the snippet.** Search snippets are truncated, and many come from third parties summarizing the doc rather than the doc itself. Open the actual page before answering from it.
- **Budget: 1–3 lookups.** On the fourth, stop and answer with what's in hand. If the query returns nothing on the right domain, say the page couldn't be located rather than substituting a third-party explainer.

Going outside these sources is fine in three cases, and name which one applies:
1. The listed sources genuinely don't cover the question — established by checking, not instead of checking.
2. Third-party benchmarks for a cross-model comparison, where Anthropic is an interested party.
3. Tool, SDK, or product mechanics — not covered here at all. Route to `product-self-knowledge`.

## Source map

Page titles are more stable than paths — the docs have already moved once and now serve from both `platform.claude.com/docs/...` and `docs.claude.com/en/docs/...`. Search the title; recognize the result by its URL shape.

**1. Prompting best practices — highest yield, start here for most questions**
Query: `site:docs.claude.com "Prompting best practices"`
URL shape: `.../build-with-claude/prompt-engineering/claude-prompting-best-practices`
The living reference. Organized as model-specific differences first, then techniques for all current models, then migration notes. Covers clarity, examples, XML structuring, role prompting, thinking, tool use, and agentic systems.
Note: *Prompt engineering overview* is a signpost that points here, not the reference. Don't stop there.

**2. Per-model prompting pages — for "why does this model behave differently"**
Query: `site:docs.claude.com "Prompting Claude <model name>"`
URL shape: `.../prompt-engineering/...` alongside source 1.
Pages exist for the current lineup (Fable 5, Opus 5, Opus 4.8, Sonnet 5 as of this writing). When the user names a model, read its page rather than generalizing from another model's.

**3. Models overview — for "which model should I use"**
Query: `site:docs.claude.com "Models overview"`
URL shape: `.../docs/about-claude/models/overview`
Context windows, output limits, thinking and tool support per model. Also linked from source 1. Half of "using Claude well" is model choice, not phrasing.

**4. System cards — the only source that *measures* behavior**
Query: `anthropic.com "<model name>" system card` — or `site:anthropic.com transparency` for the hub that links current cards.
URL shape: `anthropic.com/transparency`, `anthropic.com/<model>-system-card`, or a PDF on `www-cdn.anthropic.com`.
Use for measured capability and refusal characteristics, known failure modes, knowledge cutoff, and concrete operational boundaries. These often explain a refusal that no rephrasing will get around — worth checking before someone spends an hour prompt-engineering into a wall.
Always label as vendor-run: Anthropic designed the evals, ran them, and graded them. Report as "Anthropic measured X," not "X is true."

**5. Engineering blog — for long-context and agentic work**
Query: `site:anthropic.com/engineering <topic>`
URL shape: `anthropic.com/engineering/<post-slug>`
Especially *Effective context engineering for AI agents*, plus posts on Agent Skills, tool design, evals, long-running agents, and MCP. Reach for these when the problem is context degradation, tool sprawl, or multi-step task design rather than wording.

**6. Feature docs — mechanics that change what's possible**
Query: `site:docs.claude.com "<exact page title>"` using the titles below.
URL shape: `.../docs/build-with-claude/<page>`. Sources 1 and 2 live in this section too.

Sub-sections worth knowing:
- **Thinking** — *Overview*, *Steering and cost control*, *Tool and multi-turn workflows*, *Troubleshooting*. Note: *Extended thinking* is the **legacy** page covering manual `budget_tokens` mode. Start at *Thinking*, not there.
- **Context management** — *Context windows*, *Compaction*, *Context editing*, *Prompt caching*, *Token counting*. Go here first for long-context degradation questions; more concrete than the engineering blog.
- **Tools** — *How tool use works*, *Define tools*, *Handle tool calls*, *Parallel tool use*, *Strict tool use*, plus per-tool pages and *Troubleshooting*.
- **Tool infrastructure** — *Manage tool context*, *Tool combinations*, *Programmatic tool calling*, *Fine-grained tool streaming*. For when tool sprawl is the problem.

**7. Claude's Constitution — narrow use only**
Query: `anthropic.com/constitution` or `site:anthropic.com "Claude\'s Constitution"`
URL shape: `anthropic.com/constitution` for the readable version. The version-archived source is the `anthropics/claude-constitution` GitHub repo, but the repo landing page is mostly navigation chrome — if using it, open the dated `.md` file, not the repo root.
Consult it for exactly one thing: **the instruction-precedence model** — the priority ordering of safety, ethics, Anthropic's guidelines, and helpfulness; the operator/user trust distinction; and which defaults are instructable versus fixed. That's the only public explanation of why a system prompt gets overridden and which instructions can never work regardless of phrasing.
Do not use it as a general "how Claude works" source. See framing rules below.

**Third-party sources:** independent benchmarks and evals are legitimate for model-comparison questions, where Anthropic is an interested party — label them as third-party and name who ran them. Reddit threads, YouTube explainers, and SEO blog posts are not sources of truth here; they are confidently wrong about exactly this topic.

## Framing rules — the most common accuracy failure

Three different kinds of claim get mixed up constantly. Keep them apart in the wording of the answer:

| Source type | What it establishes | How to phrase it |
|---|---|---|
| Constitution, policy docs | Design *intent* — the training target | "Anthropic's stated intent is…" / "Claude is trained toward…" |
| Docs, prompting guides | Documented, expected behavior | "The docs say…" / "Documented behavior is…" |
| System cards, benchmarks | *Measured* behavior, by whoever ran the test | "Anthropic measured…" / "On [eval], the reported result was…" |

Quoting the constitution as if it described what the model *does* is the single most common failure — it's overclaiming laundered through a citation. Training doesn't perfectly hit its target, and a normative document is not a measurement.

## Workflow

1. **Check the boundary.** If the question is about this conversation rather than Claude in general, stop here — answer it from the conversation, outside this workflow.
2. **Classify:** prompting/technique → source 1–2. Model choice → 3. Measured behavior or hard boundary → 4. Long-context/agentic → 5. Feature mechanics → 6. Instruction precedence → 7. Product fact → hand off.
3. **Run the pinned query and open the page.** Recognize the right result by its URL shape. Answer from the page, not the snippet.
4. **Verify version-sensitive specifics even with strong background knowledge** — model names, context limits, current page structure, which behaviors are on by default.
5. **Answer and commit.** Give the direct answer first, in the format that fits the conversation. Say where it came from in one clause, not a citation block.

## When to stop

Over-searching is a real cost, and so is bottomless hedging. Calibrate:

- **Stable conceptual material** (what few-shot prompting is, why examples help, what a system prompt does): answer directly. One confirming lookup at most.
- **Version-sensitive or model-specific** (which model, current limits, per-model prompting differences, whether a feature exists): always look it up. This is the core case.
- **Budget as above: 1–3 lookups.** If that hasn't answered it, stop and answer with what you have.

**When the source doesn't cover it:** say that plainly — "the docs don't specify this" — and then give the best practical answer available, labeled as inference rather than documentation. Do not fill the gap with a plausible-sounding specific. An honest gap plus a working suggestion beats a confident invention.

**When sources conflict:** name the conflict and date it. A newer Anthropic primary source wins over an older one; when both are current, say so rather than picking silently.

## Answer shape

This runs in chat. Default to a direct conversational answer, not a report with headers and a source list. Lead with the actionable part — the prompt change, the model to switch to, the setting to flip — then the supporting detail.

State one uncertainty where it genuinely matters and then commit to a recommendation. Stacking caveats is not accuracy; it's an unusable answer wearing accuracy's clothes.

## Quick routing

- *"Why doesn't Claude follow instructions in a system prompt?"* → source 7 for precedence, source 1 for phrasing
- *"Why did you just do X in this chat?"* → out of scope. Answer from the conversation, not this skill.
- *"Best way to prompt for X?"* → source 1, then the per-model page (2)
- *"Opus or Sonnet for this?"* → source 3, plus system cards (4) for measured differences
- *"It gets worse in long conversations"* → Context management pages in source 6, then source 5 for agent design
- *"It refuses X no matter how I phrase it"* → source 4 for the documented boundary, then 7 for why it isn't rephrasable
- *"How much does this cost / what's my limit?"* → `product-self-knowledge`
