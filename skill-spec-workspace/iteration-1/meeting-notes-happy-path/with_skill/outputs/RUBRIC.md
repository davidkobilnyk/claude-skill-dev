# Rubric: Meeting Notes → Action Items

## Criteria

### 1. Triggering accuracy
Fires when someone pastes raw meeting notes (bullets, fragments, shorthand, tangents included) and asks to turn them into a list, clean them up, or pull out the action items — or pastes notes with clear meeting shape and no further instruction needed. Stays quiet on near-misses named in the spec: summarizing a non-meeting document or transcript, drafting a pre-meeting agenda, organizing a personal to-do list with no meeting behind it, or a request to actually send/post/email the output somewhere. A clear failure looks like: firing on a plain to-do list because it superficially resembles a task list, or refusing/deflecting on genuinely messy real meeting notes because they don't look like a clean input.

### 2. Extraction completeness and precision
Every genuine action item present in the notes is captured exactly once — including ones buried mid-tangent or stated only implicitly ("someone should look into X") — and nothing that isn't an action item (FYI-only updates, pure decisions with no follow-up, small talk, pasted links with no attached task) makes it into the list. A clear failure looks like: an item getting lost because it wasn't in a clean bullet, a decision-only line getting listed as if it were an action, or the same task appearing twice because it was mentioned in two places in the notes.

### 3. Correct handling of missing owner/date (no guessing)
When an owner or due date isn't stated or unambiguously inferable, the output uses the spec's exact placeholder language (`Owner: TBD – needs assignment`, `Due: No date set`) rather than inventing a plausible-sounding name or date. Vague/relative dates ("before launch," "next week") are carried through as stated, not converted into a fabricated calendar date. A clear failure looks like: quietly assigning an item to whoever seems most likely from context when the notes never actually said so, or turning "before launch" into a specific invented date.

### 4. Output format consistency
Output matches the spec's fixed structure every time: a Markdown checkbox line per item with Task — Owner — Due, grouped under topic headings when the notes clearly span multiple topics and left as a flat list when they don't (auto-detected, not asked about). A clear failure looks like: inconsistent formatting from one run to the next, grouping a single-topic sync under headings anyway (or failing to group a genuinely multi-topic planning meeting), or dropping one of the three fields (task/owner/due) on some items but not others.

### 5. Respecting scope boundaries
The output is action items only — no discussion summary, no decisions log, no minutes — and the skill never attempts to send, post, or deliver the result anywhere; it only produces text for the person to copy themselves. It also doesn't try to track or reference action items from any other meeting/run. A clear failure looks like: appending a "summary of discussion" section nobody asked for, or the output claiming/implying it was sent to Slack.

### 6. Honest handling of empty or ambiguous input
When notes genuinely contain no action items, the output says so plainly rather than fabricating items to avoid an empty result. When it's genuinely unclear whether a line is an action item, it's included with the TBD/No-date-set placeholders rather than being silently dropped. A clear failure looks like: inventing a plausible-sounding task that isn't actually in the notes just so the list isn't empty.

## Overall score (out of 10)

A 9–10 means every genuine action item was found and correctly separated from non-action content, owners and dates are handled exactly per the placeholder rules with zero invented guesses, the grouping/flat-list choice matches what the notes actually contain, the output is nothing but the action list (no summary creep, no attempted sending), and this held true even on messy, tangent-heavy, real-world-shaped notes — not just a clean example. A 5–6 means the core list is basically right but shows a real lapse: a missed or duplicated item, a guessed owner or invented date, inconsistent formatting between a grouped and flat case, or a stray summary/decisions section creeping into the output. Below that, the skill is meaningfully unreliable — for example, dropping real action items, regularly guessing at owners/dates instead of flagging them, or triggering on inputs the spec explicitly says should be left alone (a to-do list, an agenda, a non-meeting document).
