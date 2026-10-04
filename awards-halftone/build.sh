#!/usr/bin/env bash
# Rebuild the Halftone Awards into a Raytha 2.x site. Needs RAYTHA_URL and RAYTHA_API_KEY; see README.md.
# The entry artwork is generated, not stored: draw it first if seed/art/ is missing (needs python3).
[ -d "$(dirname "$0")/seed/art" ] || (cd "$(dirname "$0")/seed" && python3 make-art.py)
exec bash "$(dirname "$0")/../scripts/build-example.sh" "$(dirname "$0")"
