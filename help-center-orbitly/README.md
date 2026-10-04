# Orbitly: a SaaS help center

A knowledge base and help center for Orbitly, a fictional project planner, built on Raytha 2.0.1 by an AI agent
with the [`raytha` CLI](https://github.com/RaythaHQ/raytha-cli). Every template, content type, article, page, menu
and function went in through the CLI. Nobody opened the admin.

- **Brief:** [brief.md](brief.md)
- **Build time:** about 30 minutes of agent time, from an empty install to `raytha check` passing
- **Write-up:** [raytha.com/use-cases/orbitly-help-center](https://raytha.com/use-cases/orbitly-help-center)

![Orbitly help center home page](https://raytha.com/raytha/media-items/objectkey/yxBjCaWwv02PaLCf2EC_gg_orbitly_help_01_home_hero.webp)

## Screenshots

| | |
|---|---|
| ![Search results as you type](https://raytha.com/raytha/media-items/objectkey/N3Kh2HVnXEWuOBg601p2yw_orbitly_help_03_instant_search.webp) | ![Article page](https://raytha.com/raytha/media-items/objectkey/0CpzhI8efE-yE3uMxg8MpQ_orbitly_help_05_article.webp) |
| Results appear as you type, from a Raytha Function | Article with steps, an outline and related articles |
| ![Changelog](https://raytha.com/raytha/media-items/objectkey/YmP4nu8JKkG35O9HA51mUA_orbitly_help_09_changelog.webp) | ![Status page](https://raytha.com/raytha/media-items/objectkey/EYD3o9oCN0aMvSdfGLcplQ_orbitly_help_10_status.webp) |
| Changelog with New, Improved and Fixed filters | Status page with 90 days of uptime |

<p>
  <img src="https://raytha.com/raytha/media-items/objectkey/IBOejFjsvkWm0U1EBEKy1Q_orbitly_help_11_home_mobile.webp" width="240" alt="Home on a phone">
  <img src="https://raytha.com/raytha/media-items/objectkey/l7FF08y54UqwtV2Ij-9ZTQ_orbitly_help_12_article_mobile.webp" width="240" alt="Article on a phone">
</p>

More in [screenshots/](screenshots/). Recapture them from your own build with [shots.json](shots.json) and
[`scripts/capture-screenshots.py`](../scripts/capture-screenshots.py).

## What's in it

- A home page with a search box that suggests articles as you type, topic tiles with live article counts, the
  most-read articles, the latest releases and a contact panel.
- Six topics, each with a colour and icon, and a page per topic listing its articles in reading order.
- A search page at `/articles` that matches titles, summaries and full text and narrows by topic and tag.
- Article pages with numbered steps, tip callouts, an "On this page" outline, previous and next links, the rest of
  the topic, related articles from other topics, and `TechArticle` JSON-LD.
- A changelog at `/changelog` with a New, Improved or Fixed filter, a page per release and an RSS feed.
- A status page with 90 days of uptime per component and past incidents, all editable as widget settings.
- A restyled 404 page with a search box.

## The Raytha features behind it

| Feature | How it's built |
|---------|----------------|
| Topics, articles, releases | Three **content types** in [schema.json](schema.json). Articles have a **relationship field** to their topic, a **multiple select** for tags, a **date**, **numbers** for reading time and order, and a **checkbox** for popular. Releases have a **dropdown** for the kind of change. |
| Seed content | `raytha content import` from JSON Lines in [seed/](seed/). Each article points at its topic by name. |
| Search as you type | A **Raytha Function** at `/search.json?q=` ([functions/search.js](functions/search.js)) queries articles through `API_V1` and returns JSON. The base layout calls it as you type. |
| Search results | A **list view** at `/articles`. The **Liquid** template reads `?q=`, `?category=` and `?tag=`, checks each value and builds a filter for `get_content_items`, such as `contains(tags,'security') and category eq '<id>'`. |
| Related articles | The article template queries articles that share its first tag outside its own topic, plus the topic's articles in order for previous and next links. |
| Changelog feed | A second Function serves RSS at `/feeds/changelog.rss`. |
| Home and status pages | **Site pages** built from 6 custom **widget templates** (search hero, topic tiles, popular articles and releases, contact panel, page header, status board). |
| Navigation | Two **menus**, `mainmenu` and `footer`, in [menus/](menus/). |

## Rebuild it

You need a Raytha 2.x site you can wipe (a fresh install is best), an admin API key, the `raytha` CLI, and `jq`.
Follow steps 1 to 3 of the [Quickstart](../README.md#quickstart) to run Raytha, create a key and install the CLI, then:

```bash
cd help-center-orbitly
DRY_RUN=1 bash build.sh     # previews the schema import, changes nothing
bash build.sh
```

`build.sh` runs the shared [scripts/build-example.sh](../scripts/build-example.sh) with this folder's
[example.json](example.json). It pushes and activates the `orbitly` theme, imports the schema, binds every view to
its list template, imports the seed content, creates the two site pages, the two functions and both menus, then
runs `raytha check`. You can run it again: everything is created or updated in place, and seed content only goes
into content types that are still empty. Set `PRUNE_MENUS=0` to keep menu items that aren't in this example.

## Files

| Path | What it is |
|------|------------|
| [brief.md](brief.md) | The brief the agent got |
| [build.sh](build.sh) | Rebuild script (`RAYTHA_URL`, `RAYTHA_API_KEY` from env) |
| [example.json](example.json) | Theme name, import order and detail templates for the shared build script |
| [schema.json](schema.json) | Content types, fields, choices and views (`raytha schema import`) |
| [theme/](theme/) | The `orbitly` theme: the `ob_*` web and widget templates plus the restyled base layout and 404 page |
| [functions/](functions/) | The search and RSS functions plus `functions.json` (names, triggers, routes) |
| [seed/](seed/) | Topics, articles and releases as JSON Lines |
| [pages/](pages/) | Site page sections and `pages.json` (title, route, template) |
| [menus/](menus/) | Main and footer menu items |
| [shots.json](shots.json) | The screenshot list for `scripts/capture-screenshots.py` |

## Notes

- Orbitly and everything in the help center is fictional. Email links use `example.com`.
- Fonts: Manrope for headings and Inter for text, from Google Fonts. Bootstrap Icons load from jsDelivr, so the
  theme has no media files.
- There are no accounts, forms or payments.
- Raytha reserves routes that start with `api`, so the search function lives at `/search.json`.
