#!/usr/bin/env bash
# Guard wrapper: runs `gh` only when the call names open-renewables-sandbox.
# Usage: tools/gh-sandbox.sh <gh args...>   (every call must contain a sandbox repo or org path)
set -euo pipefail
ALLOWED="open-renewables-sandbox"
args="$*"
if [[ "$args" != *"$ALLOWED"* ]]; then
  echo "REFUSED: arguments do not name $ALLOWED: gh $args" >&2; exit 2
fi
# Reject any other open-renewables* owner anywhere in the arguments.
if echo "$args" | grep -Eo 'open-renewables[a-z0-9-]*' | grep -qvx "$ALLOWED"; then
  echo "REFUSED: arguments name another organisation: gh $args" >&2; exit 2
fi
echo "gh-sandbox: target $ALLOWED -> gh $args" >&2
exec gh "$@"
