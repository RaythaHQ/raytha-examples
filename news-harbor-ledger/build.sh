#!/usr/bin/env bash
# Rebuild the Harbor Ledger into a Raytha 2.x site. Needs RAYTHA_URL and RAYTHA_API_KEY; see README.md.
# The story illustrations are generated, not stored: draw them first if seed/art/ is missing (needs python3).
[ -d "$(dirname "$0")/seed/art" ] || (cd "$(dirname "$0")/seed" && python3 make-art.py)
exec bash "$(dirname "$0")/../scripts/build-example.sh" "$(dirname "$0")"
