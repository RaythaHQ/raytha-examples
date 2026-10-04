# Halftone Awards: an awards site with entries, nominations and past winners

The website for the Halftone Awards, a fictional international prize for illustration, design, photography and
type, built on Raytha 2.0.1 by an AI agent with the [`raytha` CLI](https://github.com/RaythaHQ/raytha-cli). Every
template, content type, entry, page, form handler and menu went in through the CLI. Nobody opened the admin.

- **Brief:** [brief.md](brief.md)
- **Build time:** about 45 minutes of agent time, from an empty install to `raytha check` passing
- **Write-up:** [raytha.com/use-cases/halftone-awards](https://raytha.com/use-cases/halftone-awards)
- **Walkthrough video:** [MP4, 35 s](https://raytha.com/raytha/media-items/objectkey/Ibglwxveok6Ukqruh0ssig_halftone_awards_walkthrough.mp4) (shot list: [walkthrough.json](walkthrough.json))

![Halftone Awards home page](https://raytha.com/raytha/media-items/objectkey/ysBc0hzkM0y7qJE-PF8QPQ_halftone_awards_01_home_hero.webp)

## Screenshots

| | |
|---|---|
| ![An entry page](https://raytha.com/raytha/media-items/objectkey/37rdVtFZd0-RqHbV9iwDOQ_halftone_awards_06_entry.webp) | ![Entry gallery](https://raytha.com/raytha/media-items/objectkey/pYzFtp4xm0KNDxFES6e33g_halftone_awards_05_gallery.webp) |
| An entry page with the artwork, entrant, medium and statement | The entry gallery, filterable by category |
| ![Past winners](https://raytha.com/raytha/media-items/objectkey/b2C4wQIZ5E6Chee77UyIPw_halftone_awards_07_winners.webp) | ![Entry form](https://raytha.com/raytha/media-items/objectkey/5P3vyYAnoEWvNlTtCIwpFQ_halftone_awards_08_apply.webp) |
| Past winners by year | The entry form, which saves a draft through a Raytha Function |

<p>
  <img src="https://raytha.com/raytha/media-items/objectkey/AxZf_G-i70uGkszdfiw7Dg_halftone_awards_13_home_mobile.webp" width="240" alt="Home on a phone">
  <img src="https://raytha.com/raytha/media-items/objectkey/pcbcsLgUUEqx_EZeaLQY2w_halftone_awards_14_entry_mobile.webp" width="240" alt="An entry on a phone">
</p>

More in [screenshots/](screenshots/). Recapture them from your own build with [shots.json](shots.json) and
[`scripts/capture-screenshots.py`](../scripts/capture-screenshots.py).

## What's in it

- A home page with the six categories and a live countdown to each deadline, a strip of this year's entries, key
  dates, last year's Grand Prix, the jury and a call to enter.
- A page for each category at `/categories/...` with the judges' brief, deadline, fee, accepted formats, this
  year's entries and past winners.
- An entry gallery at `/entries`, filterable by category, and a page for every entry with previous and next links.
- Past winners at `/winners`, grouped by year, with the Grand Prix shown large.
- An entry form at `/apply` and a nomination form at `/nominate` that really work. Submissions are checked on the
  server and saved as drafts for the team to review.
- A jury page, rules in plain language and a thank-you page.
- Deadline badges that count down ("Open · 69 days left"), turn orange in the last 30 days and switch to "Closed"
  afterwards, with no edits needed when a deadline passes.

## How the forms work

The forms on `/apply` and `/nominate` are plain HTML forms that post to two **Raytha Functions**,
[functions/apply.js](functions/apply.js) (`forms/apply`) and [functions/nominate.js](functions/nominate.js)
(`forms/nominate`). Each one:

1. Drops the submission (and still shows the thank-you page) if the hidden `website` honeypot field is filled in.
2. Trims every value to a maximum length and checks the required fields, the email address, that links start with
   `http://` or `https://`, and that the category is one of the real categories.
3. Calls `API_V1.CreateContentItem(type, true, templateId, values)` to save a **draft** in the `applications` or
   `nominations` content type. Both have unpublished list views, and drafts have no public page.
4. Redirects to `/thanks?f=apply` or `/thanks?f=nominate`, or back to the form with `?error=` and a short
   message about what to fix.

Function form posts arrive as a list of key and value pairs, so the handlers read fields with a small `param()`
helper. The template id comes from `API_V1.GetWebTemplates()`, looked up by developer name, so the handlers work
on any install.

## The Raytha features behind it

| Feature | How it's built |
|---------|----------------|
| Categories, entries, applications, nominations | Four **content types** in [schema.json](schema.json). Entries have a **relationship field** to their category, a **number** for the year, a **dropdown** for the award, an **attachment** for the artwork and a **checkbox** for featured work. Categories have a **date** field for the deadline. |
| Seed content | `raytha content import` from JSON Lines in [seed/](seed/). Entries point at their category by name; `@file:` values upload the SVG artwork. |
| Entry gallery and past winners | Two **list views** on `entries`: `/entries` (year 2026) and `/winners` (earlier years). The gallery's **Liquid** template reads `?category=`, checks it against the real categories and builds a filter for `get_content_items`. |
| Deadline countdowns | Templates write each deadline as `data-deadline="2026-12-11"`; a few lines of script in the base layout turn it into days left. |
| Entry and nomination forms | Two `http_request` **Raytha Functions** in [functions/](functions/), listed in [functions.json](functions/functions.json). |
| Private submissions | `"isPublished": false` on the `applications` and `nominations` views in [schema.json](schema.json). |
| Home, Enter, Nominate, Jury, Rules, Thank you | **Site pages** built from 11 custom **widget templates**. |
| Navigation | Two **menus**, `mainmenu` and `footer`, in [menus/](menus/). The footer also lists the categories from the content. |

## Rebuild it

You need a Raytha 2.x site you can wipe (a fresh install is best), an admin API key, the `raytha` CLI, `jq` and
`python3` (to draw the artwork).
Follow steps 1 to 3 of the [Quickstart](../README.md#quickstart) to run Raytha, create a key and install the CLI, then:

```bash
cd awards-halftone
DRY_RUN=1 bash build.sh     # previews the schema import, changes nothing
bash build.sh
```

`build.sh` first draws the 24 artwork SVGs into `seed/art/` with [seed/make-art.py](seed/make-art.py) if they are not
there yet (they are generated, so they are not stored in the repository). It then runs the shared [scripts/build-example.sh](../scripts/build-example.sh) with this folder's
[example.json](example.json). It pushes and activates the `halftone` theme, imports the schema, binds every view
to its list template (keeping the two submission views unpublished), imports the categories and entries with their
artwork, creates the six site pages, the two form functions and both menus, then runs `raytha check`. You can run it
again: everything is created or updated in place, and seed content only goes into content types that are still empty.

To try the forms, open `/apply` on your site, send an entry, then find it under Applications in the admin as a draft.

## Files

| Path | What it is |
|------|------------|
| [brief.md](brief.md) | The brief the agent got |
| [build.sh](build.sh) | Rebuild script (`RAYTHA_URL`, `RAYTHA_API_KEY` from env) |
| [example.json](example.json) | Theme name, import order and detail templates for the shared build script |
| [schema.json](schema.json) | Content types, fields, choices and views (`raytha schema import`) |
| [theme/](theme/) | The `halftone` theme: the `ht_*` web and widget templates plus the restyled base layout and 404 page |
| [functions/](functions/) | The entry and nomination form handlers and `functions.json` (name, trigger, route) |
| [seed/](seed/) | Categories and entries as JSON Lines, plus [make-art.py](seed/make-art.py), which draws the SVG artwork into `seed/art/` |
| [pages/](pages/) | Site page sections and `pages.json` (title, route, template) |
| [menus/](menus/) | Main and footer menu items |
| [shots.json](shots.json) | The screenshot list for `scripts/capture-screenshots.py` |
| [walkthrough.json](walkthrough.json) | The shot list for [`scripts/make-walkthrough.py`](../scripts/make-walkthrough.md) |

## Notes

- The Halftone Awards, the entrants, judges and entries are fictional. Email links use `example.com`. The artwork is
  generated halftone dot patterns, so every image is license-free.
- Entry fees are never taken on the site. The rules say entrants get a payment link by email after their entry is
  confirmed.
- The form endpoints are public by design. Spam protection is the honeypot plus server-side checks, and nothing is
  published without review. Add rate limiting at your proxy if you expect heavy traffic.
- Fonts: Instrument Serif for headlines, Inter for text and JetBrains Mono for labels, from Google Fonts. Bootstrap
  Icons load from jsDelivr.
- Raytha's Liquid does not support `{% include %}` of other web templates, so the entry card markup is repeated in
  the templates that list entries.
- Date fields render as an object in Liquid. Use `.Value` before the `date` filter, as in
  `{{ p.deadline.Value | date: "%-d %b %Y" }}`.
