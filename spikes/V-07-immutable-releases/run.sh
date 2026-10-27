#!/usr/bin/env bash
# V-07: enable immutable releases on the sandbox repo, publish a release with an asset, then try to change it.
# Every gh call goes through tools/gh-sandbox.sh. Output is the evidence.
set -u
R=open-renewables-sandbox/p0-spikes
G="tools/gh-sandbox.sh"
T=v0.0.3-p0
[ "$(git remote get-url origin)" = "git@github.com:$R.git" ] || { echo "origin is not the sandbox"; exit 2; }
say() { echo; echo "### $*"; }
say "enable immutable releases"; $G api -X PUT repos/$R/immutable-releases 2>&1 | head -5; echo "exit=$?"
$G api repos/$R/immutable-releases 2>&1 | tail -1; echo
say "tag and draft release with asset"
git tag -a $T -m "V-07 immutable release test" && git push origin $T 2>&1 | tail -1
printf 'asset v1\n' > /tmp/asset1.txt
$G release create $T -R $R --draft --title "V-07 $T" --notes "immutable test" /tmp/asset1.txt 2>&1 | tail -1
say "publish the draft"; $G release edit $T -R $R --draft=false 2>&1 | tail -2
$G api repos/$R/releases/tags/$T --jq '{id,draft,immutable,tag_name,assets:[.assets[].name]}' 2>&1 | tail -2
say "after publish: change release notes"; $G release edit $T -R $R --notes "changed notes" 2>&1 | tail -2
say "after publish: upload a new asset"; printf 'asset v2\n' > /tmp/asset2.txt; $G release upload $T /tmp/asset2.txt -R $R 2>&1 | tail -2
say "after publish: replace existing asset (--clobber)"; printf 'asset v1 modified\n' > /tmp/asset1.txt; $G release upload $T /tmp/asset1.txt -R $R --clobber 2>&1 | tail -2
say "after publish: delete the asset"; $G release delete-asset $T asset1.txt -R $R -y 2>&1 | tail -2
say "move the tag (force push to another commit)"; git tag -f -a $T -m moved HEAD~1 >/dev/null 2>&1; git push -f origin $T 2>&1 | tail -3
say "delete the tag"; git push origin :refs/tags/$T 2>&1 | tail -3
say "delete the release"; $G release delete $T -R $R -y 2>&1 | tail -2
say "final state"; $G api repos/$R/releases --jq '.[] | select(.tag_name=="'$T'") | {id,draft,immutable,assets:[.assets[].name]}' 2>&1 | tail -3
git ls-remote --tags origin $T | cat
