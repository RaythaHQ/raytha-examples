# Low Tide Festival: a music festival site with a lineup, schedule grid and venue map

The website for Low Tide, a fictional three-day music festival with 36 artists on four stages, built on Raytha 2.0.1
by an AI agent with the [`raytha` CLI](https://github.com/RaythaHQ/raytha-cli). Every template, content type, item,
page and menu went in through the CLI. Nobody opened the admin.

- **Brief:** [brief.md](brief.md)
- **Build time:** about an hour of agent time, from an empty install to `raytha check` passing
- **Write-up:** [raytha.com/use-cases/lowtide-festival](https://raytha.com/use-cases/lowtide-festival)
- **Walkthrough video:** [MP4, 36 s](https://raytha.com/raytha/media-items/objectkey/7dyazsM6iUqbjDM165vTUw_lowtide_festival_walkthrough.mp4) (shot list: [walkthrough.json](walkthrough.json))

![Low Tide home page](https://raytha.com/raytha/media-items/objectkey/ghlpZ1oiZECxM06Pjao6AQ_lowtide_01_home_hero.webp)

## Screenshots

| | |
|---|---|
| ![Lineup](https://raytha.com/raytha/media-items/objectkey/_qWc46kQQ0OYp5N8W1-Qgw_lowtide_03_lineup.webp) | ![Schedule grid](https://raytha.com/raytha/media-items/objectkey/JyFIqn2kIUW23H5ryW-hAg_lowtide_05_schedule.webp) |
| The lineup with day, stage and genre filters and a star on every set | The schedule grid: one column per stage, starred sets highlighted |
| ![Artist page](https://raytha.com/raytha/media-items/objectkey/PDlAjd-JXkOZPkdWGio2-w_lowtide_06_artist.webp) | ![Venue map](https://raytha.com/raytha/media-items/objectkey/Tkd7Xp98dEGX52JT8DaaiQ_lowtide_07_venue.webp) |
| An artist page with the set time, stage and the sets that follow | The venue map with stages, food, water and first aid |

<p>
  <img src="https://raytha.com/raytha/media-items/objectkey/eSeyvMDIOEW6J_me7Y7plw_lowtide_12_home_mobile.webp" width="240" alt="Home on a phone">
  <img src="https://raytha.com/raytha/media-items/objectkey/Fpu-RRRl4UqxyBB4M0saDQ_lowtide_13_lineup_mobile.webp" width="240" alt="Lineup on a phone">
  <img src="https://raytha.com/raytha/media-items/objectkey/g8X6eSG8YkWpSvzxCT1GRQ_lowtide_14_schedule_mobile.webp" width="240" alt="Schedule on a phone">
</p>

More in [screenshots/](screenshots/). Recapture them from your own build with [shots.json](shots.json) and
[`scripts/capture-screenshots.py`](../scripts/capture-screenshots.py).

## What's in it

- A home page with a live countdown, the headliners, a lineup poster for each day built from the content, a
  spotlight, the four stages, visitor basics, an FAQ preview and a call to action.
- A lineup at `/lineup`, filterable by day, stage and genre in any combination
  (`?day=fri|sat|sun`, `?stage=<stage-slug>`, `?genre=indie|rock|pop|electronic|hip_hop|soul|folk`).
- A schedule grid at `/schedule?day=fri|sat|sun`: one column per stage, sets placed by start time and sized by length.
- **My picks:** a star on every artist card, schedule slot and artist page. Picks are kept in `localStorage`, and the
  schedule's "My picks" switch fades out everything else. No account needed.
- A page per artist at `/artists/...` and per stage at `/stages/...`.
- A venue map at `/venue`: an inline SVG with the stages and venue places positioned from their map coordinates, and
  a legend that highlights one kind of place.
- An FAQ at `/faq`, grouped by category, with search as you type.
- Site pages for tickets (`/tickets`) and visitor information (`/info`).

## Tickets

The site sells nothing. Every ticket button, including the one in the menu, links to
`https://tickets.example.com/lowtide-2027`, a placeholder for an external ticketing partner, and carries an
external-link icon and a note saying so. Replace `ticket_url` and `primary_url` in [pages/](pages/) and the link in
[raytha_html_base_layout.liquid](theme/web-templates/raytha_html_base_layout.liquid),
[ft_detail_artists.liquid](theme/web-templates/ft_detail_artists.liquid),
[ft_list_faq.liquid](theme/web-templates/ft_list_faq.liquid) and [ft_detail_faqs.liquid](theme/web-templates/ft_detail_faqs.liquid) with your real ticket shop.

## How the schedule grid works

[ft_list_schedule.liquid](theme/web-templates/ft_list_schedule.liquid) is a list view on the artists, sorted by
`start_min` (minutes after noon). For each set on the chosen day it works out:

- the column, from the position of the set's stage in the stage list (sorted by `sort_order`), and
- the grid row, `(start_min - 120) / 15 + 2`, and the span, `duration / 15`, so one row is 15 minutes from 2 pm.

Number fields come through as objects, so the template uses `| append: "" | plus: 0` before doing maths. Move a
set by editing its `start_min` and `time_label`; the lineup, schedule, stage page and artist page all update.

## The Raytha features behind it

| Feature | How it's built |
|---------|----------------|
| Stages, artists, venue places, FAQs | Four **content types** in [schema.json](schema.json). Artists have a **relationship field** to their stage, **dropdowns** for day and genre, **number fields** for set start, length and poster line, a **checkbox** for headliners and an **attachment** for the artwork. |
| Seed content | `raytha content import` from JSON Lines in [seed/](seed/). Artists point at their stage by name; `@file:` values upload the SVG artwork. |
| Lineup | A **list view** sorted by poster line, with a **Liquid** template that combines three query parameters, each checked against the allowed values. |
| Schedule | A second **list view** on the same content type, sorted by start time, laid out as a CSS grid. |
| Venue map | A **list view** on the stages that also reads the venue places with `get_content_items`, positioned on an inline SVG. |
| Artist, stage, place and FAQ pages | **Detail templates** for each content type. |
| Home, Tickets, Plan your visit | **Site pages** built from 10 custom **widget templates**. |
| Navigation | Two **menus**, `mainmenu` and `footer`, in [menus/](menus/). The footer also lists the stages from the content. |

## Rebuild it

You need a Raytha 2.x site you can wipe (a fresh install is best), an admin API key, the `raytha` CLI, `jq` and
`python3` (to draw the artwork).
Follow steps 1 to 3 of the [Quickstart](../README.md#quickstart) to run Raytha, create a key and install the CLI, then:

```bash
cd music-festival-lowtide
DRY_RUN=1 bash build.sh     # previews the schema import, changes nothing
bash build.sh
```

`build.sh` first draws the 36 artist images into `seed/art/` with [seed/make-art.py](seed/make-art.py) if they are
not there yet. It then runs the shared [scripts/build-example.sh](../scripts/build-example.sh) with this folder's
[example.json](example.json): it pushes and activates the `lowtide` theme, imports the schema, binds every view to
its list template, imports the 66 seed items, creates the three site pages and both menus, then runs `raytha check`.
You can run it again: everything is created or updated in place, and seed content only goes into content types that
are still empty.

## Files

| Path | What it is |
|------|------------|
| [brief.md](brief.md) | The brief the agent got |
| [build.sh](build.sh) | Rebuild script (`RAYTHA_URL`, `RAYTHA_API_KEY` from env) |
| [example.json](example.json) | Theme name, import order and detail templates |
| [schema.json](schema.json) | Content types, fields, choices and views (`raytha schema import`) |
| [theme/](theme/) | The `lowtide` theme: `ft_*` web and widget templates, the base layout and 404 page |
| [seed/](seed/) | Stages, artists, venue places and FAQs as JSON Lines, plus [make-art.py](seed/make-art.py) |
| [pages/](pages/) | Site page sections and `pages.json` (title, route, template) |
| [menus/](menus/) | Main and footer menu items |
| [shots.json](shots.json) | The screenshot list for `scripts/capture-screenshots.py` |
| [walkthrough.json](walkthrough.json) | The shot list for [`scripts/make-walkthrough.py`](../scripts/make-walkthrough.md) |

## Notes

- Low Tide, its artists, stages and venue are fictional. Email addresses use `lowtide.example`, and ticket and listen
  links use `example.com`. The artwork is generated SVG, so every image is license-free.
- Fonts: Space Grotesk for headlines and Inter for text, from Google Fonts. Bootstrap Icons load from jsDelivr.
- The countdown on the home page counts to the `countdown_to` setting of the hero widget, in the visitor's time zone.
- Raytha's Liquid does not allow parentheses in conditions. The lineup combines its three filters with an `ok` flag
  instead, as [ft_list_lineup.liquid](theme/web-templates/ft_list_lineup.liquid) shows.
- Dropdown and checkbox values are objects in Liquid; capture them into a string first
  (`{% capture dy %}{{ p.day }}{% endcapture %}`). Checkboxes render `True`, and checkbox filters compare to
  `'true'` (`Filter="headliner eq 'true'"`).
