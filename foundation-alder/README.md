# The Alder Foundation: a foundation site with grant programs, grantees, impact stories and annual reports

The website for the Alder Foundation, a fictional grantmaking foundation in one river valley, built on Raytha 2.0.1
by an AI agent with the [`raytha` CLI](https://github.com/RaythaHQ/raytha-cli). Every template, content type, item,
page and menu went in through the CLI. Nobody opened the admin.

- **Brief:** [brief.md](brief.md)
- **Build time:** about an hour of agent time, from an empty install to `raytha check` passing
- **Write-up:** [raytha.com/use-cases/alder-foundation](https://raytha.com/use-cases/alder-foundation)
- **Walkthrough video:** [MP4, 36 s](https://raytha.com/raytha/media-items/objectkey/lkhhwl3oCUCKTjrwtUHLbA_alder_foundation_walkthrough.mp4) (shot list: [walkthrough.json](walkthrough.json))

![Alder Foundation home page](https://raytha.com/raytha/media-items/objectkey/4AfuiYBmH0SfvgHbAK9pGw_alder_01_home_hero.webp)

## Screenshots

| | |
|---|---|
| ![Grant program](https://raytha.com/raytha/media-items/objectkey/C7M_NxWpckGm8ovvYHNi0w_alder_04_program.webp) | ![Grantee database](https://raytha.com/raytha/media-items/objectkey/pR0jMxuPBEK1b19Nfr6vBw_alder_05_grantees.webp) |
| A grant program with who can apply, the deadline, grant size and its grantees | The grantee database, filterable by program, year and region |
| ![Impact story](https://raytha.com/raytha/media-items/objectkey/sTGnTXUmC06X2nPXv5MBRQ_alder_09_story.webp) | ![Annual report](https://raytha.com/raytha/media-items/objectkey/OAx8SKTTgUatOIll6Qym3A_alder_11_report.webp) |
| An impact story tied to its grantee and program | The 2025 annual report, with grants by program |

<p>
  <img src="https://raytha.com/raytha/media-items/objectkey/65SkkY4AT0WMTd96wSkdtg_alder_14_home_mobile.webp" width="240" alt="Home on a phone">
  <img src="https://raytha.com/raytha/media-items/objectkey/zNzLGDhNSE6IP1oxSBR44A_alder_15_grantees_mobile.webp" width="240" alt="Grantee filters on a phone">
  <img src="https://raytha.com/raytha/media-items/objectkey/Dn7qTT6UzUinsiyResHsvg_alder_17_report_mobile.webp" width="240" alt="Annual report on a phone">
</p>

More in [screenshots/](screenshots/). Recapture them from your own build with [shots.json](shots.json) and
[`scripts/capture-screenshots.py`](../scripts/capture-screenshots.py).

## What's in it

- A home page with the mission and values, cards for the five grant programs, the foundation's numbers, a featured
  impact story, the largest grants of the year, the latest annual report and a call to apply.
- Grant programs at `/programs` and `/programs/...`: who can apply, what it funds and doesn't, the next deadline,
  grant size and length, the program's grantees and its stories.
- A grantee database at `/grantees`, filterable by program, year and region in any combination
  (`?program=<program-slug>`, `?year=2023|2024|2025|2026`,
  `?region=upper_valley|lowlands|coast|marlow|regionwide`). The total and the bar chart by program follow the
  filters, and "Download this list (CSV)" saves the filtered rows from the browser.
- A page per grantee at `/grantees/...` with the grant, its program, related stories and other grantees.
- Impact stories at `/stories`, each related to a grantee and a program.
- Annual reports at `/reports`, with totals, highlights, the president's letter and that year's grants by program.
  "Download PDF" calls `window.print()`, and a print stylesheet turns the page into a clean PDF.
- Site pages for About (`/about`) and How to apply (`/apply`), and an applicant FAQ at `/apply/faq`.

## Applications

The site collects nothing. "Open the grants portal" on `/apply` links to `https://grants.example.org/alder`, a
placeholder for an external grants portal, with an external-link icon and a note saying so. Change `primary_url`
in [pages/apply.json](pages/apply.json) to your real portal.

## How the grantees, programs and reports fit together

- Each grantee has a **relationship field** to its program, dropdowns for `year` and `region` and a number field
  for `amount`. [al_list_grantees.liquid](theme/web-templates/al_list_grantees.liquid) reads the three query
  parameters, checks each against the allowed values, keeps the others when one changes, and sums the matching
  amounts.
- [al_detail_programs.liquid](theme/web-templates/al_detail_programs.liquid) and
  [al_detail_reports.liquid](theme/web-templates/al_detail_reports.liquid) load the grantees with
  `get_content_items` and keep the ones for that program or year, so a new grant shows up on its program page, its
  year's report and the home page without editing either.
- Report totals (granted, grants, first-time grantees, endowment) are fields on the report, because a real
  foundation publishes only some of its grants online. The report says how many of the year's grants are listed.
- Money is formatted with `| append: "" | plus: 0 | format_number: "N0" | prepend: "$"`; number fields are objects in
  Liquid until you do that.

## The Raytha features behind it

| Feature | How it's built |
|---------|----------------|
| Programs, grantees, stories, reports, FAQs | Five **content types** in [schema.json](schema.json). Grantees have a **relationship field** to their program, **dropdowns** for year and region and a **number field** for the amount. Stories relate to a grantee and a program and have an **attachment** for the illustration and a **checkbox** for featured. |
| Seed content | `raytha content import` from JSON Lines in [seed/](seed/). Grantees point at their program by name; `@file:` values upload the SVG illustrations. |
| Grantee database | A **list view** with a **Liquid** template that combines three query parameters. |
| Program, grantee, story, report and FAQ pages | **Detail templates** for each content type. |
| Home, About, How to apply | **Site pages** built from 14 custom **widget templates**. |
| Navigation | Two **menus**, `mainmenu` and `footer`, in [menus/](menus/). The footer also lists the programs from the content. |

## Rebuild it

You need a Raytha 2.x site you can wipe (a fresh install is best), an admin API key, the `raytha` CLI, `jq` and
`python3` (to draw the illustrations).
Follow steps 1 to 3 of the [Quickstart](../README.md#quickstart) to run Raytha, create a key and install the CLI, then:

```bash
cd foundation-alder
DRY_RUN=1 bash build.sh     # previews the schema import, changes nothing
bash build.sh
```

`build.sh` first draws the six story illustrations into `seed/art/` with [seed/make-art.py](seed/make-art.py) if
they are not there yet. It then runs the shared [scripts/build-example.sh](../scripts/build-example.sh) with this
folder's [example.json](example.json): it pushes and activates the `alder` theme, imports the schema, binds every
view to its list template, imports the 59 seed items, creates the three site pages and both menus, then runs
`raytha check`. You can run it again: everything is created or updated in place, and seed content only goes into
content types that are still empty.

## Files

| Path | What it is |
|------|------------|
| [brief.md](brief.md) | The brief the agent got |
| [build.sh](build.sh) | Rebuild script (`RAYTHA_URL`, `RAYTHA_API_KEY` from env) |
| [example.json](example.json) | Theme name, import order and detail templates |
| [schema.json](schema.json) | Content types, fields, choices and views (`raytha schema import`) |
| [theme/](theme/) | The `alder` theme: `al_*` web and widget templates, the base layout and 404 page |
| [seed/](seed/) | Programs, grantees, stories, reports and FAQs as JSON Lines, plus [make-art.py](seed/make-art.py) |
| [pages/](pages/) | Site page sections and `pages.json` (title, route, template) |
| [menus/](menus/) | Main and footer menu items |
| [shots.json](shots.json) | The screenshot list for `scripts/capture-screenshots.py` |
| [walkthrough.json](walkthrough.json) | The shot list for [`scripts/make-walkthrough.py`](../scripts/make-walkthrough.md) |

## Notes

- The Alder Foundation, its staff, grantees and stories are fictional. Email addresses use `alder.example`, and the
  grants portal link uses `example.org`. The story illustrations are generated SVG, so every image is license-free.
- Fonts: Newsreader for headlines and Inter Tight for text, from Google Fonts. Bootstrap Icons load from jsDelivr.
- Raytha's Liquid does not allow parentheses in conditions. The grantee filters combine with an `ok` flag instead.
- Dropdown and checkbox values are objects in Liquid; capture them into a string first. Checkboxes render `True`,
  and checkbox filters compare to `'true'` (`Filter="featured eq 'true'"`).
