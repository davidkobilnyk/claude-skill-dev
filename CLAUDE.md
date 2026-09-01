# Repo notes

## Before committing/pushing to an existing branch

This repo's workflow creates a lot of short-lived branches, each usually tracked by one PR, and work often continues on the "same" branch across multiple turns or sessions. Before adding a new commit to a branch that already had a PR opened from it (rather than a brand-new branch), check whether that PR is still open:

```
gh pr list --head <branch-name> --state all
```

or the equivalent `mcp__github__list_pull_requests` / `pull_request_read` call. If the PR is already merged or closed, a new commit pushed to that branch name will **not** land in that PR (it's already finished) — it needs a **new PR**, opened fresh from the current head.

**This check is per-push, not per-branch.** Don't treat "I already verified this branch's PR is open" as a fact that stays true for the rest of the conversation — re-run the check before *every* push, including the second, fifth, and twentieth commit in a row on a branch whose PR you personally opened ten minutes ago. A PR can merge the instant after you check it (the user merging manually, another session, a merge queue), and "I checked earlier in this session" is exactly the assumption that's failed here more than once — most recently a PR that merged 2 minutes after being opened, with half a dozen further commits pushed to the same branch afterward before anyone noticed. Skipping the recheck because it "was just confirmed a moment ago" is not a shortcut, it's the failure mode.

**Subscribe to activity on any PR you open.** Immediately after creating a pull request, call `subscribe_pr_activity` (or the equivalent GitHub MCP tool) for it. This turns a merge into a pushed notification instead of something that depends on remembering to re-poll — the check above is still required before every push regardless, but the subscription is what catches a merge in the gap between pushes rather than relying purely on manual discipline.

## PR creation on a per-project basis

Don't open a PR unless the user explicitly asks — that's the default, and it holds until they do. Once a user has explicitly asked for a PR on a given branch/project **twice** in the same conversation, treat that as durable permission to keep opening/reusing PRs for that same branch's remaining work without re-asking each time — but say so out loud the first time this kicks in (e.g. "I'll keep opening PRs on this branch as work continues, since you've asked twice now — let me know if you'd rather confirm each one"), rather than silently inferring the permission and never mentioning it. This durable permission is scoped to that one branch/project; a different branch or a new project starts the default over.
