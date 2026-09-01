# Repo notes

## Before committing/pushing to an existing branch

This repo's workflow creates a lot of short-lived branches, each usually tracked by one PR, and work often continues on the "same" branch across multiple turns or sessions. Before adding a new commit to a branch that already had a PR opened from it (rather than a brand-new branch), check whether that PR is still open:

```
gh pr list --head <branch-name> --state all
```

or the equivalent `mcp__github__list_pull_requests` / `pull_request_read` call. If the PR is already merged or closed, a new commit pushed to that branch name will **not** land in that PR (it's already finished) — it needs a **new PR**, opened fresh from the current head.

**This check is per-push, not per-branch.** Don't treat "I already verified this branch's PR is open" as a fact that stays true for the rest of the conversation — re-run the check before *every* push, including the second, fifth, and twentieth commit in a row on a branch whose PR you personally opened ten minutes ago. A PR can merge the instant after you check it (the user merging manually, another session, a merge queue), and "I checked earlier in this session" is exactly the assumption that's failed here more than once — most recently a PR that merged 2 minutes after being opened, with half a dozen further commits pushed to the same branch afterward before anyone noticed. Skipping the recheck because it "was just confirmed a moment ago" is not a shortcut, it's the failure mode.

**Subscribe to activity on any PR you open.** Immediately after creating a pull request, call `subscribe_pr_activity` (or the equivalent GitHub MCP tool) for it. This turns a merge into a pushed notification instead of something that depends on remembering to re-poll — the check above is still required before every push regardless, but the subscription is what catches a merge in the gap between pushes rather than relying purely on manual discipline.

## PR creation on every commit

The default is to open a PR after every commit that gets pushed — no need to wait for the user to ask. Before opening one, check for an already-open, unmerged PR from the same branch that this commit reasonably belongs to (the same check as the "Before committing/pushing to an existing branch" section above already surfaces this); if one exists, the push lands in it automatically and no new PR is needed. Only open a fresh PR when there is no open unmerged PR that makes sense to add the commit to — e.g. the branch has never had a PR, or its prior PR was merged/closed and this is new work continuing on the same branch name.

Immediately after opening any PR, call `subscribe_pr_activity` for it per the section above.
