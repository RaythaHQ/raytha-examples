#!/usr/bin/env bash
set -euo pipefail
D="$(cd "$(dirname "$0")" && pwd)"; RAYTHA="${RAYTHA:-raytha}"
SKIP_CHECK=1 bash "$D/../scripts/build-example.sh" "$D"
# Tidy routes made from titles such as "The Rev. Miriam Achterberg" (people/the-rev.-miriam-achterberg -> people/the-rev-miriam-achterberg)
for t in $(jq -r '.types[]' "$D/example.json"); do
  "$RAYTHA" content list "$t" --all | jq -r '.data.items[] | select(.routePath | test("[.?!,]")) | "\(.id) \(.routePath | gsub("[.?!,]+";"") | gsub("-+";"-"))"' |
  while read -r id route; do "$RAYTHA" content settings "$t" "$id" --route-path "$route" >/dev/null && echo "    route -> $route" >&2; done
done
if [[ "${SKIP_CHECK:-0}" != "1" ]]; then "$RAYTHA" check | jq -r '.data | "    route check: \(.checked) checked, \(.failed) failed, \(.warnings) warnings"' >&2; fi
