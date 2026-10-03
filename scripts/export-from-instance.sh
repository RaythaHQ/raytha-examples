#!/usr/bin/env bash
# Export a site from a Raytha instance into an example folder.
#
#   RAYTHA_URL=... RAYTHA_API_KEY=... bash scripts/export-from-instance.sh <example-folder> <theme-developer-name>
#
# Writes theme/, schema.json, functions/*.js + functions.json, pages/*.json + pages.json and menus/*.json.
# Seed content isn't exported: keep your seed JSONL and images in seed/ from the start.
# Review everything with scripts/scan-secrets.sh before committing.
set -euo pipefail
cd "$(dirname "$0")/.."
dir="${1:?usage: export-from-instance.sh <example-folder> <theme>}"; theme="${2:?theme developer name}"
: "${RAYTHA_URL:?set RAYTHA_URL}" "${RAYTHA_API_KEY:?set RAYTHA_API_KEY}"
command -v jq >/dev/null || { echo "jq is required" >&2; exit 2; }
mkdir -p "$dir"/{functions,pages,menus}

echo "theme $theme -> $dir/theme" >&2
raytha theme pull "$theme" "$dir/theme" >/dev/null

echo "schema -> $dir/schema.json" >&2
raytha schema export | jq '.data // .' > "$dir/schema.json"

echo "functions -> $dir/functions" >&2
raytha function list --all | jq -c '.data.items[]' | while read -r f; do
  dn=$(jq -r .developerName <<<"$f")
  raytha function get "$dn" | jq -r '.data.code' > "$dir/functions/$dn.js"
done
raytha function list --all | jq '[.data.items[] | {developerName, name, trigger: .triggerType.developerName, file: (.developerName + ".js"), routePath}]' > "$dir/functions/functions.json"

echo "site pages -> $dir/pages" >&2
raytha site-page list --all | jq -c '.data.items[]' | while read -r p; do
  id=$(jq -r .id <<<"$p"); route=$(jq -r .routePath <<<"$p"); file="${route//\//-}.json"
  raytha site-page get "$id" | jq '(.data.publishedWidgets // .data.widgets // {}) | with_entries(.value |= map({widgetType, settings}))' > "$dir/pages/$file"
done
raytha site-page list --all | jq '[.data.items[] | {title, routePath, template, sections: ("pages/" + (.routePath | gsub("/"; "-")) + ".json"), home: (.routePath == "home")}]' > "$dir/pages/pages.json"

echo "menus -> $dir/menus" >&2
raytha menu list --all | jq -c '.data.items[]' | while read -r m; do
  dn=$(jq -r .developerName <<<"$m"); label=$(jq -r .label <<<"$m")
  raytha menu items list "$dn" | jq --arg dn "$dn" --arg l "$label" '{developerName: $dn, label: $l, items: [.data | sort_by(.ordinal)[] | {label, link: .url}]}' > "$dir/menus/$dn.json"
done

echo "Done. Check pages/*.json against your site: section names and widget settings depend on your templates." >&2
echo "Then run scripts/scan-secrets.sh" >&2
