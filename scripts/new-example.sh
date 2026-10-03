#!/usr/bin/env bash
# Scaffold a new example folder:  bash scripts/new-example.sh <folder-name> "<Site title>"
# Folder names are kebab-case and start with the kind of site, e.g. conference-horizon-summit, restaurant-kiln-and-kettle.
set -euo pipefail
cd "$(dirname "$0")/.."
name="${1:?usage: scripts/new-example.sh <folder-name> \"<Site title>\"}"
title="${2:-$name}"
[[ "$name" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]] || { echo "folder name must be kebab-case" >&2; exit 2; }
[[ -e "$name" ]] && { echo "$name already exists" >&2; exit 2; }

mkdir -p "$name"/{theme/web-templates,theme/widget-templates,functions,seed,pages,menus,screenshots}
sed "s/<site name>/$title/" templates/brief-template.md > "$name/brief.md"
cat > "$name/theme/theme.json" <<JSON
{
  "title": "$title",
  "developerName": "${name//-/_}",
  "description": "$title theme"
}
JSON
echo '[]' > "$name/functions/functions.json"
echo '[]' > "$name/pages/pages.json"
echo '[]' > "$name/shots.json"
cat > "$name/README.md" <<MD
# $title

<!-- What it is, one screenshot, and the build time. -->

- **Brief:** [brief.md](brief.md)
- **Build time:**

## Screenshots

## What's in it

## The Raytha features behind it

| Feature | How it's built |
|---------|----------------|

## Rebuild it

\`\`\`bash
export RAYTHA_URL=... RAYTHA_API_KEY=...
DRY_RUN=1 bash build.sh && bash build.sh
\`\`\`
MD
cat > "$name/build.sh" <<'SH'
#!/usr/bin/env bash
# Rebuild this example into a Raytha site. Start from ../conference-horizon-summit/build.sh, which handles the
# theme, schema, views, seed content, pages, functions, menus and the final check idempotently.
set -euo pipefail
cd "$(dirname "$0")"
: "${RAYTHA_URL:?set RAYTHA_URL}" "${RAYTHA_API_KEY:?set RAYTHA_API_KEY}"
echo "TODO: copy and adapt ../conference-horizon-summit/build.sh" >&2
exit 1
SH
chmod +x "$name/build.sh"
echo "Created $name/. Next: fill in $name/brief.md, build the site, then run scripts/export-from-instance.sh $name <theme>"
