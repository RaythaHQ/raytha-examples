#!/usr/bin/env bash
# Rebuild an example folder into a Raytha 2.x site. Each example's build.sh calls this script.
#
#   RAYTHA_URL=https://your-site.example RAYTHA_API_KEY=... bash scripts/build-example.sh <example-folder>
#
# The folder needs example.json (theme name, content type import order, detail templates, user groups),
# schema.json, theme/, and optionally seed/<type>.jsonl, pages/pages.json, functions/functions.json, menus/*.json.
# Safe to run more than once: everything is created or updated in place, and seed content is only imported into
# content types that are still empty.
#
# Options (environment variables):
#   DRY_RUN=1      Preview the schema import, then stop without changing anything.
#   PRUNE_MENUS=0  Keep menu items that are not in menus/*.json (default: make the menus match exactly).
#   FORCE_SEED=1   Import seed content even if a content type already has items (creates duplicates).
#   SKIP_CHECK=1   Skip the final `raytha check`.
#
# Requires: raytha CLI (https://github.com/RaythaHQ/raytha-cli) and jq.
set -euo pipefail

DIR="${1:?Usage: build-example.sh <example-folder>}"
cd "$DIR"
: "${RAYTHA_URL:?Set RAYTHA_URL to your Raytha site, e.g. https://example.com}"
: "${RAYTHA_API_KEY:?Set RAYTHA_API_KEY to an admin API key (People > Admins > your account > Create API key)}"
export RAYTHA_URL RAYTHA_API_KEY
RAYTHA="${RAYTHA:-raytha}"
command -v "$RAYTHA" >/dev/null || { echo "raytha CLI not found. Install: https://github.com/RaythaHQ/raytha-cli" >&2; exit 2; }
command -v jq >/dev/null || { echo "jq not found. Install jq first." >&2; exit 2; }

THEME=$(jq -r .theme example.json)
mapfile -t TYPES < <(jq -r '.types[]' example.json)

step() { printf '\n\033[1;35m==>\033[0m %s\n' "$*" >&2; }
note() { printf '    %s\n' "$*" >&2; }
rt() {
  local out
  if ! out=$("$RAYTHA" "$@"); then echo "$out" >&2; echo "raytha $1 $2 failed" >&2; exit 1; fi
  printf '%s' "$out"
}

step "Checking the connection"
rt doctor | jq -r '.data | "    \(.url)  Raytha \(.version)  (\(.organizationName))"' >&2

if [[ "${DRY_RUN:-0}" == "1" ]]; then
  step "Dry run: schema"
  rt schema import schema.json --dry-run | jq -c '.data | {created, updated, unchanged, warnings}' >&2
  note "theme '$THEME': $(ls theme/web-templates/*.liquid | wc -l) web templates, $(ls theme/widget-templates/*.liquid 2>/dev/null | wc -l) widget templates"
  echo "Dry run only. Nothing was changed." >&2
  exit 0
fi

# 1. Theme, schema, theme again (templates bind to content types by name, so they attach on the second push)
step "Theme and content model"
rt theme push ./theme --activate >/dev/null
rt schema import schema.json | jq -r '.data | tostring' | cut -c1-300 >&2
rt theme push ./theme >/dev/null

# 2. Bind every view to the list template named in schema.json (views with "isPublished": false stay private)
step "Views: binding list templates"
jq -r '.contentTypes[] | .developerName as $t | .views[] | "\($t) \(.developerName) \(.template) \(if .isPublished == false then "false" else "true" end)"' schema.json |
while read -r t view tpl pub; do
  vid=$(rt content-type views list "$t" --all | jq -r --arg v "$view" '(.data.items // .data)[] | select(.developerName==$v) | .id')
  if [[ -n "$vid" ]]; then rt content-type views settings "$t" "$vid" --template "$tpl" --published "$pub" >/dev/null; note "$t/$view -> $tpl$([[ $pub == false ]] && echo ' (not published)')"; fi
done

# 3. Seed content (run from seed/ so @file: paths resolve), then the detail template for every item
step "Content"
for t in "${TYPES[@]}"; do
  tpl=$(jq -r --arg t "$t" '.detailTemplates[$t] // empty' example.json)
  if [[ -f "seed/$t.jsonl" ]]; then
    count=$(rt content list "$t" --page-size 1 | jq -r '.data.totalCount // 0')
    if [[ "$count" != "0" && "${FORCE_SEED:-0}" != "1" ]]; then
      note "$t: already has $count items, skipping"
    else
      (cd seed && rt content import "$t" --file "$t.jsonl" ${tpl:+--template "$tpl"} >/dev/null)
      note "$t: imported $(grep -c . "seed/$t.jsonl") items"
    fi
  fi
  if [[ -n "$tpl" ]]; then rt content assign-template "$t" --all --template "$tpl" >/dev/null; fi
  # Lowercase item URLs and drop leading dots in path segments
  rt content list "$t" --all | jq -r '.data.items[] | (.routePath|ascii_downcase|gsub("/\\.+";"/")) as $r | select(.routePath != $r) | "\(.id) \($r)"' |
  while read -r id route; do rt content settings "$t" "$id" --route-path "$route" >/dev/null; done
done

# 4. User groups for members-only pages
step "User groups"
groups=$(rt user-group list --all)
jq -c '.groups[]?' example.json | while read -r g; do
  dn=$(jq -r .developerName <<<"$g"); label=$(jq -r .label <<<"$g")
  if jq -e --arg d "$dn" '(.data.items // .data)[] | select(.developerName==$d)' <<<"$groups" >/dev/null; then note "$dn exists"
  else rt user-group create "$dn" --label "$label" >/dev/null; note "created $dn"; fi
done

# 5. Site pages (created, or updated in place by route path)
if [[ -f pages/pages.json ]]; then
  step "Site pages"
  pages_json=$(rt site-page list --all)
  jq -c '.[]' pages/pages.json | while read -r p; do
    title=$(jq -r .title <<<"$p"); route=$(jq -r .routePath <<<"$p"); tpl=$(jq -r .template <<<"$p")
    sections=$(jq -r .sections <<<"$p"); home=$(jq -r '.home // false' <<<"$p")
    id=$(jq -r --arg r "$route" '(.data.items // .data)[] | select(.routePath==$r) | .id' <<<"$pages_json" | head -n1)
    if [[ -n "$id" ]]; then
      rt site-page edit "$id" --title "$title" --template "$tpl" >/dev/null
      rt site-page sections "$id" --sections "@${sections}" --replace --publish >/dev/null
      note "updated /$route"
    else
      args=(site-page create --title "$title" --template "$tpl" --sections "@${sections}")
      [[ "$route" != "home" ]] && args+=(--route-path "$route")
      id=$(rt "${args[@]}" | jq -r '.data.id'); note "created /$route"
    fi
    if [[ "$home" == "true" ]]; then rt site-page set-home "$id" >/dev/null; note "home page -> /$route"; fi
  done
fi

# 6. Functions (created, or code updated in place)
if [[ -f functions/functions.json ]]; then
  step "Functions"
  existing=$(rt function list --all | jq -r '(.data.items // .data)[].developerName')
  jq -c '.[]' functions/functions.json | while read -r f; do
    dn=$(jq -r .developerName <<<"$f"); name=$(jq -r .name <<<"$f"); trig=$(jq -r .trigger <<<"$f")
    file="functions/$(jq -r .file <<<"$f")"; route=$(jq -r '.routePath // ""' <<<"$f")
    if grep -qx -- "$dn" <<<"$existing"; then
      rt function edit "$dn" --name "$name" --file "$file" --route-path "$route" --active true >/dev/null; note "updated $dn"
    else
      rt function create "$dn" --name "$name" --trigger "$trig" --file "$file" --route-path "$route" >/dev/null; note "created $dn"
    fi
  done
fi

# 7. Menus, in the order listed in each file
step "Menus"
menus=$(rt menu list --all | jq -r '(.data.items // .data)[].developerName')
for m in menus/*.json; do
  dn=$(jq -r .developerName "$m"); label=$(jq -r .label "$m")
  grep -qx -- "$dn" <<<"$menus" || { rt menu create "$dn" --label "$label" >/dev/null; note "created menu $dn"; }
  current=$(rt menu items list "$dn")
  if [[ "${PRUNE_MENUS:-1}" == "1" ]]; then
    jq -r --slurpfile want "$m" '.data[] | select([.url] | inside([$want[0].items[].link]) | not) | .id' <<<"$current" |
    while read -r iid; do rt menu items delete "$dn" "$iid" --yes >/dev/null; done
    current=$(rt menu items list "$dn")
  fi
  jq -c '.items[]' "$m" | while read -r it; do
    l=$(jq -r .label <<<"$it"); link=$(jq -r .link <<<"$it")
    jq -e --arg u "$link" '.data[] | select(.url==$u)' <<<"$current" >/dev/null && continue
    rt menu items create "$dn" --label "$l" --link "$link" >/dev/null
  done
  current=$(rt menu items list "$dn"); pos=0
  jq -r '.items[].link' "$m" | while read -r link; do
    pos=$((pos+1))
    iid=$(jq -r --arg u "$link" '[.data[] | select(.url==$u)][0].id // empty' <<<"$current")
    if [[ -n "$iid" ]]; then rt menu items reorder "$dn" "$iid" --position "$pos" >/dev/null; fi
  done
  note "$dn: $(jq '.items | length' "$m") items"
done

# 8. Verify
if [[ "${SKIP_CHECK:-0}" != "1" ]]; then
  step "Checking every public route"
  if out=$("$RAYTHA" check); then
    jq -r '.data | "    \(.summary // . | tostring)"' <<<"$out" | cut -c1-400 >&2
  else
    echo "$out" | jq . >&2; echo "raytha check found broken routes" >&2; exit 6
  fi
fi
step "Done. Open ${RAYTHA_URL%/}/"
