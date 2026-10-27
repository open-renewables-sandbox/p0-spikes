#!/usr/bin/env bash
# V-13 driver: fresh clone of spikes/V-13-poe-tasks, then run the I-16 / I-17 steps and record each exit code.
# Usage: V-13-run.sh <path to V-13-poe-tasks> <result file>
set -u
SRC="$1"; RES="$2"; : > "$RES"
W="$(mktemp -d)"; ORIGIN="$W/origin"; CLONE="$W/clone"
mkdir "$ORIGIN" && cp -r "$SRC/." "$ORIGIN/"
( cd "$ORIGIN" && git init -q -b main && git config user.email t@example.org && git config user.name t \
  && git add -A && git commit -q -m "seed" ) || { echo "seed|1" >> "$RES"; exit 1; }
git clone -q "$ORIGIN" "$CLONE" || { echo "clone|1" >> "$RES"; exit 1; }
cd "$CLONE" && git config user.email t@example.org && git config user.name t
step() { local name="$1"; shift; "$@" > "$W/$name.log" 2>&1; local rc=$?; echo "$name|$rc" >> "$RES"; return 0; }
step uv-version uv --version
step poe-list uv run poe
step poe-install uv run poe install
step poe-check uv run poe check
step poe-test uv run poe test
step poe-shell-probe uv run poe shell-probe
echo "# touch" >> scripts/validate_profile.py
git add -A
step hook-commit git commit -m "trigger hooks"
{ echo "--- hook log"; cat "$W/hook-commit.log"; } >> "$RES"
for f in poe-install poe-check poe-shell-probe; do { echo "--- $f"; head -c 1500 "$W/$f.log"; echo; } >> "$RES"; done
echo "workdir $W"
