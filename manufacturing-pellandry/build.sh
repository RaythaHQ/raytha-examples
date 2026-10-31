#!/usr/bin/env bash
# Builds the example (generates the product drawings and art first if seed/art is missing), then runs the route check.
set -euo pipefail
D="$(cd "$(dirname "$0")" && pwd)"; RAYTHA="${RAYTHA:-raytha}"
[ -d "$D/seed/art" ] || (cd "$D/seed" && python3 make-art.py)
SKIP_CHECK=1 bash "$D/../scripts/build-example.sh" "$D"
if [[ "${SKIP_CHECK:-0}" != "1" ]]; then "$RAYTHA" check | jq -r '.data | "    route check: \(.checked) checked, \(.failed) failed, \(.warnings) warnings"' >&2; fi
