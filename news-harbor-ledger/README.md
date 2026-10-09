# The Harbor Ledger: a local news site with sections, bylines, a breaking banner, live updates and feeds

The website for the Harbor Ledger, a fictional nonprofit newsroom in the coastal city of Port Merrow, built on Raytha
2.0.1 by an AI agent with the [`raytha` CLI](https://github.com/RaythaHQ/raytha-cli). Every template, content type,
item, page, menu and function went in through the CLI. Nobody opened the admin.

- **Brief:** [brief.md](brief.md)
- **Build time:** about an hour of agent time, from an empty install to `raytha check` passing
- **Write-up:** [raytha.com/use-cases/harbor-ledger](https://raytha.com/use-cases/harbor-ledger)
- **Walkthrough video:** [MP4, 35 s](https://raytha.com/raytha/media-items/objectkey/1_Sl05emvkSkn4xPU4Gy8g_harbor_ledger_walkthrough.mp4) (shot list: [walkthrough.json](walkthrough.json))

![Harbor Ledger front page](https://raytha.com/raytha/media-items/objectkey/pirXNL723U29DwHo6u8cDQ_ledger_01_home_hero.webp)

## Screenshots

| | |
|---|---|
| ![Live updates](https://raytha.com/raytha/media-items/objectkey/guKuxx5h5U6S39K64CTJ3Q_ledger_04_live_updates.webp) | ![Latest news, filtered](https://raytha.com/raytha/media-items/objectkey/Z9NDF5UGXUmrX8ohTULD_w_ledger_07_latest_filtered.webp) |
| Live updates on the storm story, with key developments, official statements and a correction | Latest news filtered to Harbor & Climate news stories |
| ![Reporter page](https://raytha.com/raytha/media-items/objectkey/P3AO9Bd6k0mZu3VOZuaKHA_ledger_10_staff_page.webp) | ![Most read](https://raytha.com/raytha/media-items/objectkey/JeWwjUSOPEij-WNfy0gP8Q_ledger_12_most_read.webp) |
| A reporter's page with their beat, bio, email and stories | Most read, with a note on where the numbers come from |

<p>
  <img src="https://raytha.com/raytha/media-items/objectkey/ahGLJcKrBE6g4EGd11WIzg_ledger_15_home_mobile.webp" width="240" alt="Front page on a phone">
  <img src="https://raytha.com/raytha/media-items/objectkey/XmJ43YCITEWBkyrD-8ynzQ_ledger_16_live_mobile.webp" width="240" alt="Live updates on a phone">
  <img src="https://raytha.com/raytha/media-items/objectkey/r2EwH2vHWE26CkwnbDwXCg_ledger_18_most_read_mobile.webp" width="240" alt="Most read on a phone">
</p>

More in [screenshots/](screenshots/). Recapture them from your own build with [shots.json](shots.json) and
[`scripts/capture-screenshots.py`](../scripts/capture-screenshots.py).

## What's in it

- A newspaper-style front page: the latest headlines, the top story (the newest article with "Top story" ticked)
  with its three newest live updates, secondary stories, section rows and columns, a most-read band, opinion and the
  feeds.
- A red **breaking banner** on every page whenever an article has "Breaking" ticked. It links to the story and shows
  a pulsing "Live" marker if the story has live updates. It hides itself on the story it links to.
- Articles at `/news/...` with section, story type, byline, date and time, minutes to read, lead image and caption,
  dateline, an optional correction note, an author box, most read and more from the section.
- **Live updates** on any article with "Has live updates" ticked: timestamped, newest first, typed as update, key
  development, official statement or correction, each with a source. "Key developments" filters the list in the
  browser. All updates are also at `/live`, and each has its own page at `/live/...`.
- Latest news at `/news`, filterable by section and story type in any combination
  (`?section=<section-slug>`, `?type=news|analysis|feature|opinion|explainer`) and grouped by day.
- Section fronts at `/section/...` and an index at `/sections`.
- A page per reporter at `/staff/...` and the masthead at `/staff`.
- Most read at `/most-read`: the top ten by the "Reads in the last 7 days" field.
- An **RSS 2.0 feed** at `/feeds/latest.rss` and a **JSON Feed 1.1** at `/feeds/latest.json`, both taking
  `?section=<section-slug>`.
- An About page (`/about`) with the newsroom's standards and staff.

## How the breaking banner, live updates, most read and feeds work

- [raytha_html_base_layout.liquid](theme/web-templates/raytha_html_base_layout.liquid) runs
  `get_content_items(ContentType="articles", Filter="breaking eq 'true'", OrderBy="published_on desc", PageSize=1)`
  on every page. Ticking the checkbox on any article turns the banner on site-wide; unticking it turns it off.
- `live_updates` is its own content type with a **relationship field** to its article, a `sequence` number for
  order, a `time_label` and a `kind` dropdown. [hl_detail_articles.liquid](theme/web-templates/hl_detail_articles.liquid)
  loads the updates sorted by `sequence desc` and keeps the ones whose story is this article. Posting an update is
  one content item, with the article's id in `story` (the seed file can use the headline instead; the importer
  looks it up):
  `raytha content create live_updates --template hl_detail_live_updates --data '{"title":"...","story":"<article id>","sequence":15,"kind":"update","time_label":"11:05 PM","posted_on":"2026-10-03","body":"..."}'`.
- **Most read** is a second list view on `articles`, sorted by the `reads` number field. Raytha does not count page
  views, so the numbers here are seeded. In production, a scheduled job would write counts from your analytics into
  the field with the API; the page carries a note saying so.
- The feeds are two **Functions** with HTTP triggers, in [functions/](functions/). They read the newest 200
  articles, keep the requested section, sort by date and the time stamp (Port Merrow is on US Eastern time), and
  return RSS or JSON Feed. Their routes don't start with `api/`, which Raytha reserves.

## The Raytha features behind it

| Feature | How it's built |
|---------|----------------|
| Sections, staff, articles, live updates | Four **content types** in [schema.json](schema.json). Articles have **relationship fields** to section and author, a **dropdown** for story type, **checkboxes** for breaking, live and top story, a **number field** for reads, a **date**, an **attachment** and **rich text**. Live updates relate to their article. |
| Seed content | `raytha content import` from JSON Lines in [seed/](seed/). Articles point at their section and author by name; `@file:` values upload the SVG illustrations. |
| Breaking banner | A filtered `get_content_items` call in the **base layout**. |
| Latest news and most read | Two **list views** on `articles` with **Liquid** templates. |
| Article, section, staff and live update pages | **Detail templates** for each content type. |
| RSS and JSON Feed | Two **Functions** with HTTP triggers. |
| Front page and About | **Site pages** built from 10 custom **widget templates**. |
| Navigation | Two **menus**, `mainmenu` (the section bar) and `footer`, in [menus/](menus/). The footer also lists the sections from the content. |

## Rebuild it

[![Deploy on Railway](https://railway.com/button.svg)](https://raytha.com/go/railway?from=examples-news-harbor-ledger)

Deploy Raytha first, then import this kit. The button deploys a fresh Raytha with PostgreSQL on Railway; finish the setup wizard, create an API key, and run `build.sh` below against the new site.

You need a Raytha 2.x site you can wipe (a fresh install is best), an admin API key, the `raytha` CLI, `jq` and
`python3` (to draw the illustrations).
Follow steps 1 to 3 of the [Quickstart](../README.md#quickstart) to run Raytha, create a key and install the CLI, then:

```bash
cd news-harbor-ledger
DRY_RUN=1 bash build.sh     # previews the schema import, changes nothing
bash build.sh
```

`build.sh` first draws the 20 story illustrations into `seed/art/` with [seed/make-art.py](seed/make-art.py) if
they are not there yet. It then runs the shared [scripts/build-example.sh](../scripts/build-example.sh) with this
folder's [example.json](example.json): it pushes and activates the `ledger` theme, imports the schema, binds every
view to its list template, imports the 45 seed items, creates the two site pages, both functions and both menus,
then runs `raytha check`. You can run it again: everything is created or updated in place, and seed content only
goes into content types that are still empty.

## Files

| Path | What it is |
|------|------------|
| [brief.md](brief.md) | The brief the agent got |
| [build.sh](build.sh) | Rebuild script (`RAYTHA_URL`, `RAYTHA_API_KEY` from env) |
| [example.json](example.json) | Theme name, import order and detail templates |
| [schema.json](schema.json) | Content types, fields, choices and views (`raytha schema import`) |
| [theme/](theme/) | The `ledger` theme: `hl_*` web and widget templates, the base layout and 404 page |
| [seed/](seed/) | Sections, staff, articles and live updates as JSON Lines, plus [make-art.py](seed/make-art.py) |
| [functions/](functions/) | The RSS and JSON Feed functions and `functions.json` (name, trigger, route) |
| [pages/](pages/) | Site page sections and `pages.json` (title, route, template) |
| [menus/](menus/) | Main and footer menu items |
| [shots.json](shots.json) | The screenshot list for `scripts/capture-screenshots.py` |
| [walkthrough.json](walkthrough.json) | The shot list for [`scripts/make-walkthrough.py`](../scripts/make-walkthrough.md) |

## Notes

- The Harbor Ledger, Port Merrow, its staff and its stories are fictional. Email addresses use
  `harborledger.example`. The story illustrations are generated SVG, so every image is license-free.
- Fonts: Source Serif 4 for headlines and story text and Inter for the interface, from Google Fonts. Bootstrap
  Icons load from jsDelivr.
- Times are a text field (`time_label`, like "9:40 PM") next to a date field, because Raytha date fields hold a day.
- Raytha's Liquid does not allow parentheses in conditions. The news filters combine with an `ok` flag instead.
- Dropdown and checkbox values are objects in Liquid; capture them into a string first. Checkboxes render `True`,
  and checkbox filters compare to `'true'` (`Filter="breaking eq 'true'"`). Empty text fields can be null, so the
  templates capture and `strip` them before comparing to `""`.
