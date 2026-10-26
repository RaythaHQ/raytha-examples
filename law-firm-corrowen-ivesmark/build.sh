#!/usr/bin/env bash
# Builds the example, then removes the dot from "v." in matter URLs (e.g. matters/a-v.-b -> matters/a-v-b) and runs the route check.
set -euo pipefail
D="$(cd "$(dirname "$0")" && pwd)"; RAYTHA="${RAYTHA:-raytha}"
[ -d "$D/seed/art" ] || (cd "$D/seed" && python3 make-art.py)
SKIP_CHECK=1 bash "$D/../scripts/build-example.sh" "$D"
"$RAYTHA" content list matters --all | jq -r '.data.items[] | (.routePath|gsub("\\.";"")) as $r | select(.routePath != $r) | "\(.id) \($r)"' |
while read -r id route; do "$RAYTHA" content settings matters "$id" --route-path "$route" >/dev/null; echo "    matters: /$route" >&2; done
if [[ "${SKIP_CHECK:-0}" != "1" ]]; then "$RAYTHA" check | jq -r '.data | "    route check: \(.checked) checked, \(.failed) failed, \(.warnings) warnings"' >&2; fi
