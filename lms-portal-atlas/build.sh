#!/usr/bin/env bash
# Rebuild Atlas Learning into a Raytha 2.x site. Needs RAYTHA_URL and RAYTHA_API_KEY; see README.md.
exec bash "$(dirname "$0")/../scripts/build-example.sh" "$(dirname "$0")"
