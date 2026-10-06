#!/usr/bin/env bash
# Rebuild Meridian Hub into a Raytha 2.x site. Needs RAYTHA_URL and RAYTHA_API_KEY; see README.md.
[ -d "$(dirname "$0")/seed/art" ] || (cd "$(dirname "$0")/seed" && python3 make-art.py)
exec bash "$(dirname "$0")/../scripts/build-example.sh" "$(dirname "$0")"
