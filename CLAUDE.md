# Repo notes

## Before committing/pushing to an existing branch

This repo's workflow creates a lot of short-lived branches, each usually tracked by one PR, and work often continues on the "same" branch across multiple turns or sessions. Before adding a new commit to a branch that already had a PR opened from it (rather than a brand-new branch), check whether that PR is still open:

```
gh pr list --head <branch-name> --state all
```

or the equivalent `mcp__github__list_pull_requests` / `pull_request_read` call. If the PR is already merged or closed, a new commit pushed to that branch name will **not** land in that PR (it's already finished) — it needs a **new PR**, opened fresh from the current head. Don't assume a branch's PR is still open just because you opened it earlier in the same conversation; PRs can merge in the background (the user merging manually, another session, etc.) between when you last checked and now.
