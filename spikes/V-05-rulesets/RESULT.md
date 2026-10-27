# V-05 Rulesets, check naming, approvals, concurrency, forks: result (partial)

Date: 2026-10-27. Labels: **[Test]**, **[Doc]**. Repository `open-renewables-sandbox/p0-spikes` (public, free organisation). To protect the spike's own `main`, the ruleset targets a stand-in branch `v05-main` (`ruleset.json`; ruleset id 25934950). Workflows: `.github/workflows/validate.yml`, `concurrency-probe.yml`. Raw evidence: PR [#1](https://github.com/open-renewables-sandbox/p0-spikes/pull/1), workflow runs 40453362197 to 40453388884 (5d), 40453530756 and 40453589091 (5b).

## Outcome by sub-item

| Sub-item | Status | Result |
| --- | --- | --- |
| 5a bypass modes | **half done** | Admin bypass "for pull requests only" confirmed. App "always" half needs the GitHub App (owner) |
| 5b required-check naming | **done** | See below |
| 5c API shape | **partly done** | Admin-bypass merge recorded. Approval, stale approval and `commit_id` of an approving review need a non-author reviewer (owner, D-2) |
| 5d concurrency | **done** | Confirms the W-05 inference |
| 5e fork privacy | **done, documentation only** | Cannot be made private [Doc] |

## 5a Ruleset on a free organisation **[Test]**

A ruleset was created through the API on the public repository: require a pull request with 1 approval, squash merges only, required check `validate`, no deletion or force push; bypass list: repository role Admin (actor 5), mode `pull_request`.

- A **direct push** to the protected branch by the admin was refused: `push declined due to repository rule violations`.
- A plain `gh pr merge --squash` was refused while the approval was missing (merge state `BLOCKED`, review decision `REVIEW_REQUIRED`).
- `gh pr merge --squash --admin` **merged without an approval**: the bypass applies to a pull request merge only, as SDD §11 says.
- Not tested: the revision App on the bypass list in mode "always", which needs the owner to create the App.

## 5b Required-check naming **[Test]**

`validate.yml` (workflow name `validate-workflow`, job `validate`) runs on `pull_request` and on `pull_request_review`.

- The check run is named **`validate`** (the job name) for both events; the workflow name does not appear. One ruleset entry `validate` matches both.
- Every run adds a **new** check run with the same name on the same head commit: after the pull request run and four review-triggered runs there were five `validate` runs on one commit.
- **The newest run decides.** With the approval requirement set to 0 (to isolate the check): latest `validate` success with an earlier failure present gave merge state `CLEAN`; a new review-triggered run that failed gave `BLOCKED`; a later passing run gave `CLEAN` again.
- A comment review ("COMMENTED") is enough to trigger the `pull_request_review` run, so the author can trigger it without a second person.
- Consequence for W-04: a failing review-run blocks merging until a later run passes, and an old failure does not.

## 5c API shape after the admin bypass merge **[Test, partial]**

- `pulls/{n}`: `merged:true`, `merged_by` = the merging admin, `user` = the author (here the same person), `head.sha` `c5def15`, `merge_commit_sha` `caed351`.
- `pulls/{n}/reviews`: only `COMMENTED` reviews, each with `commit_id` equal to the head at the time (`c5def15`). There is no approval and no automatic "merged without approval" marker anywhere; it must be inferred, as AD-11 states.
- The squash commit: one parent, `committer` "GitHub", `author` the pull request author, message `<title> (#1)`.
- **`GET /commits/{sha}/pulls` returned `[]` immediately after the merge and `[1]` about 20 seconds later.** The revision writer, which runs on the push event, must retry or fall back to the `(#n)` in the squash message or to `pulls?state=closed&base=…` (which listed `merge_commit_sha` `caed351` at once). W-05 step "per commit: pull request" assumes the first.

## 5d Concurrency **[Test]**

Group `revision`, `cancel-in-progress: false`, four dispatches about 5 seconds apart, each job holding the group 45 seconds:

| Dispatch | Result |
| --- | --- |
| 1 | ran to completion |
| 2 | **cancelled** while pending |
| 3 | **cancelled** while pending |
| 4 | stayed pending, then ran to completion |

So at most one run is in progress and one pending; each newer queued run cancels the earlier pending one, as SDD §3 and W-05 assume. Catch-up processing is therefore required, not optional.

## 5e Fork of a public repository **[Doc]**

GitHub's documentation states that a fork's visibility follows its upstream and "you cannot change the visibility of a fork by itself". A fork of a public repository is public, so W-01's fork row (not a supported instantiation route) is confirmed. No test was run; a fork needs an account outside the sandbox organisation (D-3 default: documentation only).

## Feeds

SDD §11 and the W-05 inference are confirmed with one correction to note: the commit-to-pull-request lookup can lag the push. **P-5 is triggered in a small form** (W-05 wording and the writer's lookup), not for AD-11, AD-12 or §11. 5a's App half and 5c's approval cases remain open until the owner supplies the App and a reviewer.

## State left in the sandbox

Ruleset `v05-main` (id 25934950) on branch `v05-main` remains active for the App and reviewer tests; branches `v05-pr1` and `v05-main` and tag `v0.0.3-p0` exist (the tag cannot be removed, since it is immutable).
