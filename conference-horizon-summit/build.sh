#!/usr/bin/env bash
# Rebuild the Horizon Summit 2027 example into a Raytha 2.x site.
#
#   RAYTHA_URL=https://your-site.example RAYTHA_API_KEY=... bash build.sh
#
# Safe to run more than once: the theme, schema, pages, functions, menus and group are created or updated
# in place, and seed content is only imported into content types that are still empty.
#
# Options (environment variables):
#   DRY_RUN=1          Preview the theme push and schema import, then stop without changing anything.
#   PRUNE_MENUS=0      Keep menu items that are not in menus/*.json. The default (1) makes the main and
#                      footer menus match this example exactly, which is what you want on a fresh install.
#   FORCE_SEED=1       Import seed content even if a content type already has items (creates duplicates).
#   SKIP_CHECK=1       Skip the final `raytha check`.
#
# Requires: raytha CLI (https://github.com/RaythaHQ/raytha-cli) and jq.
set -euo pipefail

cd "$(dirname "$0")"
: "${RAYTHA_URL:?Set RAYTHA_URL to your Raytha site, e.g. https://example.com}"
: "${RAYTHA_API_KEY:?Set RAYTHA_API_KEY to an admin API key (Settings > Administrators > API keys)}"
export RAYTHA_URL RAYTHA_API_KEY
RAYTHA="${RAYTHA:-raytha}"
command -v "$RAYTHA" >/dev/null || { echo "raytha CLI not found. Install: https://github.com/RaythaHQ/raytha-cli" >&2; exit 2; }
command -v jq >/dev/null || { echo "jq not found. Install jq first." >&2; exit 2; }

THEME=horizon
TYPES=(tracks speakers sponsors news sessions)   # import order: sessions reference speakers and tracks

step() { printf '\n\033[1;35m==>\033[0m %s\n' "$*" >&2; }
note() { printf '    %s\n' "$*" >&2; }
# Run the CLI; on failure print its JSON error and stop.
rt() {
  local out
  if ! out=$("$RAYTHA" "$@"); then echo "$out" >&2; echo "raytha $1 $2 failed" >&2; exit 1; fi
  printf '%s' "$out"
}

step "Checking the connection"
rt doctor | jq -r '.data | "    \(.url)  Raytha \(.version)  (\(.organizationName))"' >&2

if [[ "${DRY_RUN:-0}" == "1" ]]; then
  step "Dry run: theme"
  if rt theme list --all | jq -e --arg t "$THEME" '(.data.items // .data)[] | select(.developerName==$t)' >/dev/null; then
    rt theme push ./theme --dry-run | jq -c '.data.summary' >&2
  else
    note "theme '$THEME' does not exist yet: it would be created with $(ls theme/web-templates/*.liquid | wc -l) web templates and $(ls theme/widget-templates/*.liquid | wc -l) widget templates"
  fi
  step "Dry run: schema"
  rt schema import schema.json --dry-run | jq -c '.data | {created, updated, unchanged, warnings}' >&2
  echo "Dry run only. Nothing was changed." >&2
  exit 0
fi

# 1. Theme. Pushed twice: templates are bound to content types by name, and those types only exist
#    after the schema import, so the second push attaches them.
step "Theme: pushing ./theme and activating it"
rt theme push ./theme --activate >/dev/null

# 2. Content model
step "Schema: importing 5 content types and 6 views"
rt schema import schema.json | jq -r '.data | tostring' | cut -c1-300 >&2
rt theme push ./theme >/dev/null

# 3. Views: set each view's list template explicitly (the schema names it, but set it anyway so the
#    view never falls back to the default list template).
step "Views: binding list templates"
for t in "${TYPES[@]}"; do
  tpl="hz_list_${t}"
  rt content-type views list "$t" --all | jq -r '.data.items[]? // .data[]? | .id' | while read -r vid; do
    rt content-type views settings "$t" "$vid" --template "$tpl" --published true >/dev/null
    note "$t view $vid -> $tpl"
  done
done

# 4. Seed content. Runs from seed/ so the @file: paths resolve.
step "Content: importing seed data"
pushd seed >/dev/null
for t in "${TYPES[@]}"; do
  count=$(rt content list "$t" --page-size 1 | jq -r '.data.totalCount // 0')
  if [[ "$count" != "0" && "${FORCE_SEED:-0}" != "1" ]]; then
    note "$t: already has $count items, skipping (FORCE_SEED=1 to import anyway)"
  else
    res=$(rt content import "$t" --file "seed-${t}.jsonl" --template "hz_detail_${t}")
    note "$t: $(jq -r '.data | "\(.created // .createdCount // .succeeded // "?") created, \((.failed // .failures // []) | if type=="array" then length else . end) failed"' <<<"$res")"
  fi
  # Make sure every item renders with its Horizon detail template.
  rt content assign-template "$t" --all --template "hz_detail_${t}" >/dev/null
done
popd >/dev/null

# 5. Lowercase item URLs (route paths come from the primary field, e.g. "speakers/Maya-Okafor").
step "Content: lowercasing item URLs"
for t in "${TYPES[@]}"; do
  rt content list "$t" --all | jq -r '.data.items[] | select(.routePath != (.routePath|ascii_downcase)) | "\(.id) \(.routePath|ascii_downcase)"' |
  while read -r id route; do
    rt content settings "$t" "$id" --route-path "$route" >/dev/null
    note "$t: /$route"
  done
done

# 6. User group for the members-only Attendee Hub
step "User group: attendees"
if rt user-group list --all | jq -e '(.data.items // .data)[] | select(.developerName=="attendees")' >/dev/null; then
  note "exists"
else
  rt user-group create attendees --label Attendees >/dev/null; note "created"
fi

# 7. Site pages (created, or updated in place by route path)
step "Site pages"
pages_json=$(rt site-page list --all)
jq -c '.[]' pages/pages.json | while read -r p; do
  title=$(jq -r .title <<<"$p"); route=$(jq -r .routePath <<<"$p"); tpl=$(jq -r .template <<<"$p")
  sections=$(jq -r .sections <<<"$p"); home=$(jq -r .home <<<"$p")
  id=$(jq -r --arg r "$route" '(.data.items // .data)[] | select(.routePath==$r) | .id' <<<"$pages_json" | head -n1)
  if [[ -n "$id" ]]; then
    rt site-page edit "$id" --title "$title" --template "$tpl" >/dev/null
    rt site-page sections "$id" --sections "@${sections}" --replace --publish >/dev/null
    note "updated /$route"
  else
    args=(site-page create --title "$title" --template "$tpl" --sections "@${sections}")
    [[ "$route" != "home" ]] && args+=(--route-path "$route")
    id=$(rt "${args[@]}" | jq -r '.data.id')
    note "created /$route"
  fi
  if [[ "$home" == "true" ]]; then rt site-page set-home "$id" >/dev/null; note "home page -> /$route"; fi
done

# 8. Functions (created, or code updated in place)
step "Functions"
existing=$(rt function list --all | jq -r '(.data.items // .data)[].developerName')
jq -c '.[]' functions/functions.json | while read -r f; do
  dn=$(jq -r .developerName <<<"$f"); name=$(jq -r .name <<<"$f"); trig=$(jq -r .trigger <<<"$f")
  file="functions/$(jq -r .file <<<"$f")"; route=$(jq -r .routePath <<<"$f")
  if grep -qx -- "$dn" <<<"$existing"; then
    rt function edit "$dn" --name "$name" --file "$file" --route-path "$route" --active true >/dev/null; note "updated $dn -> /$route"
  else
    rt function create "$dn" --name "$name" --trigger "$trig" --file "$file" --route-path "$route" >/dev/null; note "created $dn -> /$route"
  fi
done

# 9. Menus
step "Menus"
menus=$(rt menu list --all | jq -r '(.data.items // .data)[].developerName')
for m in menus/*.json; do
  dn=$(jq -r .developerName "$m"); label=$(jq -r .label "$m")
  if ! grep -qx -- "$dn" <<<"$menus"; then rt menu create "$dn" --label "$label" >/dev/null; note "created menu $dn"; fi
  current=$(rt menu items list "$dn")
  if [[ "${PRUNE_MENUS:-1}" == "1" ]]; then
    jq -r --slurpfile want "$m" '.data[] | select([.url] | inside([$want[0].items[].link]) | not) | "\(.id) \(.url)"' <<<"$current" |
    while read -r iid url; do rt menu items delete "$dn" "$iid" --yes >/dev/null; note "$dn: removed $url"; done
    current=$(rt menu items list "$dn")
  fi
  jq -c '.items[]' "$m" | while read -r it; do
    l=$(jq -r .label <<<"$it"); link=$(jq -r .link <<<"$it")
    if jq -e --arg u "$link" '.data[] | select(.url==$u)' <<<"$current" >/dev/null; then continue; fi
    rt menu items create "$dn" --label "$l" --link "$link" >/dev/null; note "$dn: added $l"
  done
done

# 10. Verify
if [[ "${SKIP_CHECK:-0}" != "1" ]]; then
  step "Checking every public route"
  if out=$("$RAYTHA" check); then
    jq -r '.data | "    \(.summary // . | tostring)"' <<<"$out" | cut -c1-400 >&2
  else
    echo "$out" | jq . >&2; echo "raytha check found broken routes" >&2; exit 6
  fi
fi

step "Done. Open ${RAYTHA_URL%/}/"
