# Postmark Trips: a surprise travel agency site with trip tiers, past reveals and a clue envelope

The website for Postmark Trips, a fictional surprise travel agency in Chicago, built on Raytha 2.0.1 by an AI agent
with the [`raytha` CLI](https://github.com/RaythaHQ/raytha-cli). Every template, content type, trip, review, page,
function and menu went in through the CLI. Nobody opened the admin.

- **Brief:** [brief.md](brief.md)
- **Build time:** about 50 minutes of agent time, from an empty install to `raytha check` passing
- **Write-up:** [raytha.com/use-cases/postmark-trips](https://raytha.com/use-cases/postmark-trips)
- **Walkthrough video:** [MP4, 40 s](https://raytha.com/raytha/media-items/objectkey/4hPyDoV7ekOOo_YWwd3Ekg_postmark_trips_walkthrough.mp4) (shot list: [walkthrough.json](walkthrough.json))

![Postmark Trips home page](https://raytha.com/raytha/media-items/objectkey/sJNessfzGUO96Rpjk_RQ2w_postmark_trips_01_home_hero.webp)

## Screenshots

| | |
|---|---|
| ![Trips and prices](https://raytha.com/raytha/media-items/objectkey/rKfTBQMe8kuIFF6DVOFYUQ_postmark_trips_04_trips.webp) | ![Past reveals](https://raytha.com/raytha/media-items/objectkey/bA7WWT_TtUKX9v4RFn5xSg_postmark_trips_06_reveals.webp) |
| Four tiers as stamps with guide prices, information only | Past reveals as postcards with a region filter |
| ![Reviews](https://raytha.com/raytha/media-items/objectkey/BnyhRnfnJ0yupSZnKLoMMw_postmark_trips_08_reviews.webp) | ![Trip planner](https://raytha.com/raytha/media-items/objectkey/i6BmltBfiES10xjI5uEsSA_postmark_trips_11_plan.webp) |
| Average rating and breakdown worked out in Liquid | The trip planner, which saves private drafts |

<p>
  <img src="https://raytha.com/raytha/media-items/objectkey/FYIYJKyy_UWj_Q1Gfsn_iw_postmark_trips_13_home_mobile.webp" width="240" alt="Home on a phone">
  <img src="https://raytha.com/raytha/media-items/objectkey/UHSagRzMQUuPpnW7szCv_g_postmark_trips_15_reveals_mobile.webp" width="240" alt="Reveals on a phone">
</p>

More in [screenshots/](screenshots/). Recapture them from your own build with [shots.json](shots.json) and
[`scripts/capture-screenshots.py`](../scripts/capture-screenshots.py).

## What's in it

- A home page with a sealed airmail envelope that opens to a clue from a past trip (click again for the answer,
  and again for a new clue), how it works in four steps, the tiers as stamps, three flip cards, recent reviews and
  a gift call to action.
- How it works at `/how-it-works`, from the questions to the envelope at the gate.
- Trips and prices at `/trips`: four tiers (Weekender, Classic, Long Haul, Wildcard) with guide prices per person,
  nights, reach and what is included, plus a comparison table. Each tier has its own page listing the past trips
  taken at that tier. Prices are information only.
- Past reveals at `/reveals`: 14 postcards with the clue, who went, when and their reaction, filterable with
  `?region=americas|europe|asia|africa|oceania`, each with a destination story.
- Reviews at `/reviews` with the average rating, a star breakdown and the number of gifted trips, and an FAQ at
  `/faq` grouped by topic.
- A gift page at `/gift` that describes giving a mystery trip and links to `/plan?gift=1`.
- A trip planner at `/plan`. Requests are checked on the server and saved as drafts that only the agency can read.
  There are no payments anywhere.

## How the clue envelope works

[functions/clue.js](functions/clue.js) is a `GET` **Raytha Function** at `/clue.json`. It reads the `reveals` with
`API_V1.GetContentItems`, picks one at random (or the one given by `?n=`) and returns the clue, the destination,
the country, when, who travelled, their reaction and the URL of the story. A few lines of JavaScript in the base
layout fetch it when the envelope is clicked. New reveals added in the admin join the pool straight away.

## How the trip planner works

The form on `/plan` posts to [functions/plan.js](functions/plan.js) (`forms/plan`). It:

1. Drops the submission (and still shows the thank-you page) if the hidden `website` honeypot field is filled in.
2. Trims every value to a maximum length and checks the name, email address and home airport, that the tier is one
   of the four, that there are one to eight travellers and, when "this is a gift" is ticked, that there is a
   recipient. Interests from the checkboxes are kept only if they are on the known list.
3. Calls `API_V1.CreateContentItem("trip_requests", true, templateId, values)` to save a **draft**. The
   `trip_requests` view is unpublished and drafts have no public page.
4. Redirects to `/plan/thanks?name=Priya` (with `&gift=1` for gifts), or back to the form with `?error=`.

The template id is looked up with `API_V1.GetWebTemplates("pm_detail_private", "", 1, 200)`. Called with no
arguments, `GetWebTemplates()` returns only the first 50 templates across all themes.

## The Raytha features behind it

| Feature | How it's built |
|---------|----------------|
| Tiers, reveals, reviews, FAQs, trip requests | Five **content types** in [schema.json](schema.json). Tiers have a **checkbox** for the most popular and a **color**; reveals a **dropdown** region, a **one-to-one relationship** to their tier and an **attachment** postcard; reviews a **number** rating and a gift **checkbox**. |
| Seed content | `raytha content import` from JSON Lines in [seed/](seed/). Reveals and reviews point at their tier by name, and `@file:` values upload the SVG postcards. |
| Trips, reveals, reviews, FAQ | Four public **list views** with their own **Liquid** templates. The reviews template adds up ratings and gifts as it renders. |
| Clue JSON and trip planner | Two `http_request` **Raytha Functions** in [functions/](functions/), listed in [functions.json](functions/functions.json). |
| Tier and reveal pages | **Detail templates**. A tier page finds its reveals with `get_content_items(ContentType="reveals", Filter="tier eq '<id>'")`. |
| Home, How it works, Gift, Plan, Thank you | **Site pages** built from 10 custom **widget templates**. |
| Navigation | Two **menus**, `mainmenu` and `footer`, in [menus/](menus/). |

## Rebuild it

You need a Raytha 2.x site you can wipe (a fresh install is best), an admin API key, the `raytha` CLI, `jq` and
`python3` (to draw the postcards).
Follow steps 1 to 3 of the [Quickstart](../README.md#quickstart) to run Raytha, create a key and install the CLI, then:

```bash
cd travel-postmark
DRY_RUN=1 bash build.sh     # previews the schema import, changes nothing
bash build.sh
```

`build.sh` first draws the postcards into `seed/art/` with [seed/make-art.py](seed/make-art.py) if they are not there
yet (they are generated, so they are not stored in the repository). It then runs the shared
[scripts/build-example.sh](../scripts/build-example.sh) with this folder's [example.json](example.json). It pushes and
activates the `postmark` theme, imports the schema, binds every view to its list template (keeping trip requests
unpublished), imports the content, creates the five site pages, the two functions and both menus, then runs
`raytha check`. You can run it again: everything is created or updated in place, and seed content only goes into
content types that are still empty.

## Files

| Path | What it is |
|------|------------|
| [brief.md](brief.md) | The brief the agent got |
| [build.sh](build.sh) | Rebuild script (`RAYTHA_URL`, `RAYTHA_API_KEY` from env) |
| [example.json](example.json) | Theme name, import order and detail templates for the shared build script |
| [schema.json](schema.json) | Content types, fields, choices and views (`raytha schema import`) |
| [theme/](theme/) | The `postmark` theme: the `pm_*` web and widget templates and the base layout |
| [functions/](functions/) | The trip planner handler, the clue JSON and `functions.json` (name, trigger, route) |
| [seed/](seed/) | Tiers, reveals, reviews and FAQs as JSON Lines, plus [make-art.py](seed/make-art.py) and [art.json](seed/art.json), which draw the postcards into `seed/art/` |
| [pages/](pages/) | Site page sections and `pages.json` (title, route, template) |
| [menus/](menus/) | Main and footer menu items |
| [shots.json](shots.json) | The screenshot list for `scripts/capture-screenshots.py` |
| [walkthrough.json](walkthrough.json) | The shot list for [`scripts/make-walkthrough.py`](../scripts/make-walkthrough.md) |

## Notes

- Postmark Trips, its travellers and reviews are fictional. The destinations are real. Email addresses and the
  phone number are placeholders.
- Prices are guide prices shown for information only. Every trip is quoted by email; there is no checkout and no
  payment form, and the gift option is described rather than sold.
- The planner endpoint is public by design. Spam protection is the honeypot plus server-side checks, and nothing is
  published. Add rate limiting at your proxy if you expect heavy traffic.
- The envelope and flip cards work with a keyboard (Enter or Space) as well as a click, and their motion stops when
  the visitor asks for reduced motion.
- Fonts: Young Serif for headlines, Manrope for text and Space Mono for labels, from Google Fonts. Bootstrap Icons
  load from jsDelivr.
- A fresh install also has an About page and a `posts` content type. The build leaves them alone; delete them if you
  don't need them.
