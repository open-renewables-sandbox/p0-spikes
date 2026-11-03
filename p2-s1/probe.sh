#!/usr/bin/env bash
# P2 step 1 probe. Runs in GitHub Actions in the sandbox only. Synthetic content.
set -uo pipefail
mkdir -p out
API="repos/$REPO"
RUN="${GITHUB_RUN_ID:-0}"
CASE_NAME="${CASE#p2-s1/run-}"

gh_app() { GH_TOKEN="$APP_TOKEN" gh "$@"; }
gh_act() { GH_TOKEN="$ACTIONS_TOKEN" gh "$@"; }
ms() { date +%s%3N; }
scrub() { sed -e "s#${APP_TOKEN}#<app-token>#g" -e "s#${ACTIONS_TOKEN}#<actions-token>#g"; }
set_remote() { git remote set-url origin "https://x-access-token:$1@github.com/${REPO}.git"; }

git config user.name "p2-s1-probe"
git config user.email "p2-s1@example.invalid"
git fetch -q origin main

probe_5a() {
  git checkout -q -B s1-main origin/main
  mkdir -p p2-s1
  echo "5a app push $RUN" > p2-s1/5a-app.txt
  git add p2-s1/5a-app.txt
  git commit -qm "p2-s1: 5a push with the app token"
  set_remote "$APP_TOKEN"
  git push origin HEAD:main 2>&1 | scrub > out/5a-app-push.txt
  echo "exit=${PIPESTATUS[0]}" >> out/5a-app-push.txt

  echo "5a actions-token push $RUN" > p2-s1/5a-actions.txt
  git add p2-s1/5a-actions.txt
  git commit -qm "p2-s1: 5a push with GITHUB_TOKEN"
  set_remote "$ACTIONS_TOKEN"
  git push origin HEAD:main 2>&1 | scrub > out/5a-actions-push.txt
  echo "exit=${PIPESTATUS[0]}" >> out/5a-actions-push.txt

  gh_app api "$API/rules/branches/main" > out/5a-rules-main.json 2>&1
  gh_app api "$API/commits/main" --jq '{sha: .sha, author: .author.login, committer: .committer.login, message: .commit.message}' > out/5a-main-head.json 2>&1
}

lookup() { # id pr sha
  local id=$1 pr=$2 sha=$3 t0 t m1 m2 m3 i
  t0=$(ms)
  printf 'ms_since_merge\tclosed_list\tsubject\tcommit_pulls\n' > "out/$id-lookup.tsv"
  for i in $(seq 1 45); do
    t=$(( $(ms) - t0 ))
    m1=$(gh_app api "$API/pulls?state=closed&sort=updated&direction=desc&per_page=30" --jq "[.[] | select(.merge_commit_sha == \"$sha\") | .number] | first // empty" 2>/dev/null)
    m2=$(gh_app api "$API/commits/$sha" --jq '.commit.message' 2>/dev/null | head -1 | sed -n 's/.*(#\([0-9][0-9]*\))$/\1/p')
    m3=$(gh_app api "$API/commits/$sha/pulls" --jq '.[0].number // empty' 2>/dev/null)
    printf '%s\t%s\t%s\t%s\n' "$t" "$m1" "$m2" "$m3" >> "out/$id-lookup.tsv"
    if [ -n "$m1" ] && [ -n "$m2" ] && [ -n "$m3" ]; then break; fi
    sleep 2
  done
}

pr_cycle() { # id with_review(1|0)
  local id=$1 review=$2 br pr headA headB sha
  br="p2-s1/pr-$id-$RUN"
  git checkout -q -B "$br" origin/main
  mkdir -p p2-s1
  echo "pr $id commit A $RUN" > "p2-s1/$id.txt"
  git add "p2-s1/$id.txt"
  git commit -qm "p2-s1: $id commit A"
  set_remote "$APP_TOKEN"
  git push -q origin "$br" 2>&1 | scrub > "out/$id-push-a.txt"
  headA=$(git rev-parse HEAD)
  pr=$(gh_app api "$API/pulls" -f title="p2-s1 $id" -f head="$br" -f base=main -f body="synthetic" --jq .number)
  echo "$pr" > "out/$id-pr-number.txt"
  gh_app api "$API/issues/$pr/labels" -f 'labels[]=approved-move' > "out/$id-labels.json" 2>&1
  if [ "$review" = "1" ]; then
    gh_act api "$API/pulls/$pr/reviews" -f event=APPROVE -f commit_id="$headA" -f body="synthetic approval" > "out/$id-review-post.json" 2>&1
  fi
  echo "pr $id commit B $RUN" >> "p2-s1/$id.txt"
  git add "p2-s1/$id.txt"
  git commit -qm "p2-s1: $id commit B"
  git push -q origin "$br" 2>&1 | scrub > "out/$id-push-b.txt"
  headB=$(git rev-parse HEAD)
  printf '{"head_a":"%s","head_b":"%s"}\n' "$headA" "$headB" > "out/$id-heads.json"
  sleep 3
  gh_app api "$API/pulls/$pr/reviews" > "out/$id-reviews.json" 2>&1
  gh_app api "$API/pulls/$pr" > "out/$id-pr-before.json" 2>&1
  gh_app api "$API/pulls/$pr/files" > "out/$id-files.json" 2>&1
  gh_app api -X PUT "$API/pulls/$pr/merge" -f merge_method=squash > "out/$id-merge.json" 2>&1
  sha=$(sed -n 's/.*"sha": *"\([0-9a-f]*\)".*/\1/p' "out/$id-merge.json" | head -1)
  echo "merge_sha=$sha" > "out/$id-merge-sha.txt"
  gh_app api "$API/pulls/$pr" > "out/$id-pr-after.json" 2>&1
  [ -n "$sha" ] && lookup "$id" "$pr" "$sha"
  git fetch -q origin main
}

case "$CASE_NAME" in
  5a-push)   probe_5a ;;
  5c-review) pr_cycle stale 1; pr_cycle noreview 0 ;;
  lookup)    pr_cycle lk1 0; pr_cycle lk2 0; pr_cycle lk3 0 ;;
  *) echo "unknown case $CASE_NAME" >&2; exit 2 ;;
esac
ls -l out
