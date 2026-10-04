# Maren & Ezra: a wedding website with a schedule, hotel blocks and a working RSVP

The wedding website for Maren & Ezra, a fictional couple getting married at an orchard in the Hudson Valley, built
on Raytha 2.0.1 by an AI agent with the [`raytha` CLI](https://github.com/RaythaHQ/raytha-cli). Every template,
content type, event, hotel, page, function and menu went in through the CLI. Nobody opened the admin.

- **Brief:** [brief.md](brief.md)
- **Build time:** about 40 minutes of agent time, from an empty install to `raytha check` passing
- **Write-up:** [raytha.com/use-cases/maren-ezra-wedding](https://raytha.com/use-cases/maren-ezra-wedding)
- **Walkthrough video:** [MP4, 36 s](https://raytha.com/raytha/media-items/objectkey/i_3WFE8xnE-bJVinoQkQSA_maren_ezra_wedding_walkthrough.mp4) (shot list: [walkthrough.json](walkthrough.json))

![Maren & Ezra home page](https://raytha.com/raytha/media-items/objectkey/C0SAAyOVg0WlEbppl3brpQ_maren_ezra_wedding_01_home_hero.webp)

## Screenshots

| | |
|---|---|
| ![The weekend schedule](https://raytha.com/raytha/media-items/objectkey/gHjL6X8Dt0KDTG5MJeNyew_maren_ezra_wedding_03_schedule.webp) | ![RSVP form](https://raytha.com/raytha/media-items/objectkey/AS0bd9j3FUmc8qzMGkghsA_maren_ezra_wedding_10_rsvp.webp) |
| The weekend schedule, with dress codes, maps and add-to-calendar links | The RSVP form, which saves a private draft through a Raytha Function |
| ![Travel and hotels](https://raytha.com/raytha/media-items/objectkey/LF76BTW7HUyTnLKlxhxV3w_maren_ezra_wedding_05_travel.webp) | ![Guest page](https://raytha.com/raytha/media-items/objectkey/O3etDbJlHUitVvgKYSTbEA_maren_ezra_wedding_12_guests.webp) |
| Hotel room blocks with a countdown to each cut-off | The guest page, rendered only for signed-in guests |

<p>
  <img src="https://raytha.com/raytha/media-items/objectkey/kHcD4Cn330KhLJ9yG5uzIw_maren_ezra_wedding_14_home_mobile.webp" width="240" alt="Home on a phone">
  <img src="https://raytha.com/raytha/media-items/objectkey/omz8quq08E622Uj7LrVIxg_maren_ezra_wedding_15_schedule_mobile.webp" width="240" alt="The schedule on a phone">
</p>

More in [screenshots/](screenshots/). Recapture them from your own build with [shots.json](shots.json) and
[`scripts/capture-screenshots.py`](../scripts/capture-screenshots.py).

## What's in it

- A home page with the couple's names, the date and place, a live countdown to the ceremony, a welcome note, the
  weekend at a glance, the first story chapters, gallery postcards and a call to RSVP.
- A three-day schedule at `/schedule`, grouped by day, with the time, venue, address, dress code, a map link and an
  add-to-calendar link for every event, plus a page for each event.
- A travel page at `/travel` with train, plane and car directions and room blocks at three hotels. Each card shows
  the group rate and booking code, whether the shuttle stops there, and how long until the block closes.
- Things to do at `/things-to-do`, filterable by kind, each with a note from the couple.
- The couple's story in six illustrated chapters, an FAQ grouped by topic, a registry page whose cards open each
  registry on its own site, and a gallery with a lightbox.
- An RSVP form at `/rsvp` that really works. Replies are checked on the server and saved as drafts that only the
  couple can read.
- A guest page at `/guests` with shuttle times, day-of contacts, the after-party, the photo album link and a
  babysitter list, rendered only for signed-in members of the `guests` group. The after-party is on the schedule
  too, but only for signed-in guests.
- Calendar files for the whole weekend (`/calendar.ics`) and for each event (`/calendar.ics?id=...`).

## How the RSVP works

The form on `/rsvp` is a plain HTML form that posts to a **Raytha Function**, [functions/rsvp.js](functions/rsvp.js)
(`forms/rsvp`). It:

1. Drops the submission (and still shows the thank-you page) if the hidden `website` honeypot field is filled in.
2. Refuses replies after the RSVP deadline (`DEADLINE` at the top of the file).
3. Trims every value to a maximum length and checks the name, the email address and the yes or no answer. For a
   yes, it also checks that the party size is 1 to 6 and the dinner choice is one of the four options, and keeps
   only event names that really are on the public schedule (checkbox values arrive as one key with several values).
4. Calls `API_V1.CreateContentItem("rsvps", true, templateId, values)` to save a **draft**. The `rsvps` view is
   unpublished and drafts have no public page.
5. Redirects to `/rsvp/thanks?a=yes&name=Sam` (or `a=no`), or back to the form with `?error=` and a short message.

The template id is looked up with `API_V1.GetWebTemplates("wb_detail_private", "", 1, 200)`. Called with no
arguments, `GetWebTemplates()` returns only the first 50 templates across all themes, and on a fresh install with
this theme the one you want can be on the second page.

[functions/calendar.js](functions/calendar.js) (`calendar.ics`) builds the `.ics` files from the `events` content
type. Events marked "only for signed-in guests" are never included.

## The Raytha features behind it

| Feature | How it's built |
|---------|----------------|
| Story, schedule, hotels, places, FAQ, registry, gallery, RSVPs | Eight **content types** in [schema.json](schema.json). Events have a **dropdown** for the day and a **checkbox** for guests-only events; hotels a **date** for the block cut-off, a **checkbox** for the shuttle and a **color** for the card; places and questions a **dropdown** for kind and topic; story chapters and photos an **attachment**. |
| Seed content | `raytha content import` from JSON Lines in [seed/](seed/). `@file:` values upload the SVG illustrations. |
| Schedule, things to do, FAQ, registry, gallery, story | Six **list views**, each with its own **Liquid** template. The things-to-do template checks `?kind=` against the known kinds before building a filter for `get_content_items`. |
| Guest page and guests-only events | A **user group** (`guests`, created from [example.json](example.json)). [wb_guests.liquid](theme/web-templates/wb_guests.liquid) and [wb_list_events.liquid](theme/web-templates/wb_list_events.liquid) check `CurrentUser.UserGroups` on the server. The sign-in templates are restyled to match. |
| RSVP and calendar files | Two `http_request` **Raytha Functions** in [functions/](functions/), listed in [functions.json](functions/functions.json). |
| Countdowns | The hero writes the ceremony time as `data-countdown`, hotel cards write `data-cutoff`, and a few lines of script in the base layout keep them current. |
| Home, Travel, RSVP, Thank you, Guest page | **Site pages** built from 12 custom **widget templates**. |
| Navigation | Two **menus**, `mainmenu` and `footer`, in [menus/](menus/). |

## Rebuild it

You need a Raytha 2.x site you can wipe (a fresh install is best), an admin API key, the `raytha` CLI, `jq` and
`python3` (to draw the illustrations).
Follow steps 1 to 3 of the [Quickstart](../README.md#quickstart) to run Raytha, create a key and install the CLI, then:

```bash
cd wedding-maren-ezra
DRY_RUN=1 bash build.sh     # previews the schema import, changes nothing
bash build.sh
```

`build.sh` first draws the 18 illustrations into `seed/art/` with [seed/make-art.py](seed/make-art.py) if they are not
there yet (they are generated, so they are not stored in the repository). It then runs the shared
[scripts/build-example.sh](../scripts/build-example.sh) with this folder's [example.json](example.json). It pushes and
activates the `willowbank` theme, imports the schema, binds every view to its list template (keeping the RSVPs view
unpublished), imports the content with its illustrations, creates the `guests` user group, the five site pages, the
two functions and both menus, then runs `raytha check`. You can run it again: everything is created or updated in
place, and seed content only goes into content types that are still empty.

To see the guest page, create a guest and give them a password (never use an admin account for this):

```bash
GROUP=$(raytha user-group list | jq -r '(.data.items // .data)[] | select(.developerName=="guests") | .id')
ID=$(raytha user create --email guest@example.com --first-name Sam --last-name Rivera --groups "$GROUP" | jq -r .data.id)
raytha user password "$ID" --password-stdin    # type a password, then Ctrl-D
```

To try the RSVP, open `/rsvp` on your site, send a reply, then find it under RSVPs in the admin as a draft.

## Files

| Path | What it is |
|------|------------|
| [brief.md](brief.md) | The brief the agent got |
| [build.sh](build.sh) | Rebuild script (`RAYTHA_URL`, `RAYTHA_API_KEY` from env) |
| [example.json](example.json) | Theme name, import order, detail templates and the user group for the shared build script |
| [schema.json](schema.json) | Content types, fields, choices and views (`raytha schema import`) |
| [theme/](theme/) | The `willowbank` theme: the `wb_*` web and widget templates plus the restyled base layout, sign-in and 404 pages |
| [functions/](functions/) | The RSVP handler, the calendar feed and `functions.json` (name, trigger, route) |
| [seed/](seed/) | Story, events, hotels, places, questions, registries and photos as JSON Lines, plus [make-art.py](seed/make-art.py), which draws the illustrations into `seed/art/` |
| [pages/](pages/) | Site page sections and `pages.json` (title, route, template) |
| [menus/](menus/) | Main and footer menu items |
| [shots.json](shots.json) | The screenshot list for `scripts/capture-screenshots.py` (the guest page shot needs `LOGIN_EMAIL` and `LOGIN_PASSWORD` for a guest) |
| [walkthrough.json](walkthrough.json) | The shot list for [`scripts/make-walkthrough.py`](../scripts/make-walkthrough.md) |

## Notes

- Maren, Ezra, Willowbank, the hotels, shops and restaurants, the planner and every phone number are fictional.
  Hudson, Germantown and the other towns are real, as are Kaaterskill Falls, Olana and Poets' Walk Park. Email
  addresses use `example.com` and booking and registry links point at `example.com`.
- The pictures are illustrated landscapes drawn by [seed/make-art.py](seed/make-art.py), so every image is
  license-free and no real people appear on the site.
- There are no payment forms. Registry cards link out to each registry's own site.
- The RSVP endpoint is public by design. Spam protection is the honeypot plus server-side checks, and nothing is
  published. Add rate limiting at your proxy if you expect heavy traffic.
- `CurrentUser` is available in web templates but not inside widget templates, so the guest check lives in the page
  and list templates. The schedule teaser widget on the home page always leaves guests-only events out.
- Fonts: Cormorant Garamond for headlines and Figtree for text, from Google Fonts. Bootstrap Icons load from jsDelivr.
- A fresh install also has an About page and a `posts` content type. The build leaves them alone; delete them if you
  don't need them.
