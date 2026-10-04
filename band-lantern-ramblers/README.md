# Lantern Ramblers: a tribute band site with tour dates, a setlist archive and live song stats

The website for Lantern Ramblers, a fictional Grateful Dead tribute band from Asheville, North Carolina, built on
Raytha 2.0.1 by an AI agent with the [`raytha` CLI](https://github.com/RaythaHQ/raytha-cli). Every template,
content type, show, setlist, page, function and menu went in through the CLI. Nobody opened the admin.

- **Brief:** [brief.md](brief.md)
- **Build time:** about 45 minutes of agent time, from an empty install to `raytha check` passing
- **Write-up:** [raytha.com/use-cases/lantern-ramblers](https://raytha.com/use-cases/lantern-ramblers)
- **Walkthrough video:** [MP4, 38 s](https://raytha.com/raytha/media-items/objectkey/wKhcWTQbC0OPJaPvBSbscw_lantern_ramblers_walkthrough.mp4) (shot list: [walkthrough.json](walkthrough.json))

![Lantern Ramblers home page](https://raytha.com/raytha/media-items/objectkey/gk6fvObkGECGJo67ivubyg_lantern_ramblers_01_home_hero.webp)

## Screenshots

| | |
|---|---|
| ![Tour](https://raytha.com/raytha/media-items/objectkey/r82zCDkguUGgws6TOmT33g_lantern_ramblers_03_tour.webp) | ![Song stats](https://raytha.com/raytha/media-items/objectkey/hgIAP-B-F0i3i2HBAGCT7w_lantern_ramblers_04_songs.webp) |
| Upcoming shows with ticket status, and past shows that file themselves | Song stats counted live from every setlist |
| ![Setlist archive filtered to one song](https://raytha.com/raytha/media-items/objectkey/0Xe4GI-JnUawAEFJVGlTdA_lantern_ramblers_06_setlists_song.webp) | ![Booking](https://raytha.com/raytha/media-items/objectkey/x7Ze11u6fEWkYP4eAMqNug_lantern_ramblers_12_booking.webp) |
| Click any song to see the nights it was played | Booking info and an inquiry form that saves private drafts |

<p>
  <img src="https://raytha.com/raytha/media-items/objectkey/Aje9RP7fnkiWJ1yTFp7cDQ_lantern_ramblers_13_home_mobile.webp" width="240" alt="Home on a phone">
  <img src="https://raytha.com/raytha/media-items/objectkey/9Jzk66vj5kK6yH4gACbD0Q_lantern_ramblers_15_songs_mobile.webp" width="240" alt="Song stats on a phone">
</p>

More in [screenshots/](screenshots/). Recapture them from your own build with [shots.json](shots.json) and
[`scripts/capture-screenshots.py`](../scripts/capture-screenshots.py).

## What's in it

- A home page with the next show and its poster, the next five dates, a most-played songs chart, the band, the
  latest setlist, recent media and a booking call to action.
- A tour page at `/tour` with upcoming shows (venue, city, door times, ages, ticket status and a link to the venue's
  ticket page) and past shows, each linking to its setlist.
- A setlist archive at `/setlists`, filterable by year (`?year=2026`) or by song (`?song=Bertha`), with segues
  marked and every song clickable.
- Song stats at `/songs`: totals, a top ten chart, openers, encores and a searchable table of every song played.
  The same numbers as JSON at `/songs.json` (and `/songs.json?song=Bertha` for one song's dates).
- Band pages at `/band`, a media page at `/media` (photos, videos and recordings, filterable with `?kind=`), and a
  page for every show, setlist, member and photo.
- A booking page at `/booking` with an inquiry form. Inquiries are checked on the server and saved as drafts that
  only the band can read. There are no payments anywhere.

## How the tour page sorts itself

There is one `tour` list view over `shows`, sorted by date. [lr_list_tour.liquid](theme/web-templates/lr_list_tour.liquid)
captures today with `"now" | date: "%Y-%m-%d"` and compares it with each show's `date.Value` formatted the same way,
so a show is listed as upcoming until its date has passed and as a past show after that. The home page hero and the
next shows widget use the same comparison.

## How the song stats work

Each setlist stores its sets as long text, one song per line, with `>` at the end of a line for a segue.
[lr_list_songs.liquid](theme/web-templates/lr_list_songs.liquid) is a second list view (`songs`) over the same
`setlists` content type. It walks every setlist, appends each song to one string as a `|Song|` token, takes the
unique songs, and counts each one by splitting the string on its token. Counts are padded (`1000 + n`) so a plain
`sort | reverse` ranks them. Drums and Space are left out. [lr_song_teaser.liquid](theme/widget-templates/lr_song_teaser.liquid)
does the same for the home page chart, and [functions/songs.js](functions/songs.js) does it in JavaScript for
`/songs.json`.

## How the booking form works

The form on `/booking` posts to a **Raytha Function**, [functions/booking.js](functions/booking.js) (`forms/booking`). It:

1. Drops the submission (and still shows the thank-you page) if the hidden `website` honeypot field is filled in.
2. Trims every value to a maximum length and checks the name, email address, message and kind of event, and that a
   requested date is not in the past.
3. Calls `API_V1.CreateContentItem("booking_requests", true, templateId, values)` to save a **draft**. The
   `booking_requests` view is unpublished and drafts have no public page.
4. Redirects to `/booking/thanks?name=Dana`, or back to the form with `?error=` and a short message.

The template id is looked up with `API_V1.GetWebTemplates("lr_detail_private", "", 1, 200)`. Called with no
arguments, `GetWebTemplates()` returns only the first 50 templates across all themes.

## The Raytha features behind it

| Feature | How it's built |
|---------|----------------|
| Shows, setlists, band, media, booking requests | Five **content types** in [schema.json](schema.json). Shows have a **date**, a **dropdown** for ticket status and an **attachment** for the poster; setlists a **one-to-one relationship** to their show and **long text** sets; members a **color**. |
| Seed content | `raytha content import` from JSON Lines in [seed/](seed/). Setlists point at their show by its title, and `@file:` values upload the SVG artwork. |
| Tour, setlists, song stats, band, media | Five public **list views** with their own **Liquid** templates; `setlists` has two views (`setlists` and `songs`). |
| Stats JSON and booking | Two `http_request` **Raytha Functions** in [functions/](functions/), listed in [functions.json](functions/functions.json). |
| Show, setlist, member, media pages | **Detail templates**. A past show finds its setlist with `get_content_items(ContentType="setlists", Filter="show eq '<id>'")`. |
| Home, Booking, Thank you | **Site pages** built from 11 custom **widget templates**. |
| Navigation | Two **menus**, `mainmenu` and `footer`, in [menus/](menus/). |

## Rebuild it

You need a Raytha 2.x site you can wipe (a fresh install is best), an admin API key, the `raytha` CLI, `jq` and
`python3` (to draw the artwork).
Follow steps 1 to 3 of the [Quickstart](../README.md#quickstart) to run Raytha, create a key and install the CLI, then:

```bash
cd band-lantern-ramblers
DRY_RUN=1 bash build.sh     # previews the schema import, changes nothing
bash build.sh
```

`build.sh` first draws the posters, photos and portraits into `seed/art/` with [seed/make-art.py](seed/make-art.py)
if they are not there yet (they are generated, so they are not stored in the repository). It then runs the shared
[scripts/build-example.sh](../scripts/build-example.sh) with this folder's [example.json](example.json). It pushes and
activates the `ramblers` theme, imports the schema, binds every view to its list template (keeping booking requests
unpublished), imports the content, creates the three site pages, the two functions and both menus, then runs
`raytha check`. You can run it again: everything is created or updated in place, and seed content only goes into
content types that are still empty.

The seed has shows from December 2025 to March 2027. As those dates pass, upcoming shows move to the past list on
their own; add new shows in the admin or append rows to [seed/shows.jsonl](seed/shows.jsonl) before you build.

## Files

| Path | What it is |
|------|------------|
| [brief.md](brief.md) | The brief the agent got |
| [build.sh](build.sh) | Rebuild script (`RAYTHA_URL`, `RAYTHA_API_KEY` from env) |
| [example.json](example.json) | Theme name, import order and detail templates for the shared build script |
| [schema.json](schema.json) | Content types, fields, choices and views (`raytha schema import`) |
| [theme/](theme/) | The `ramblers` theme: the `lr_*` web and widget templates and the base layout |
| [functions/](functions/) | The booking handler, the song stats JSON and `functions.json` (name, trigger, route) |
| [seed/](seed/) | Shows, setlists, members and media as JSON Lines, plus [make-art.py](seed/make-art.py) and [art.json](seed/art.json), which draw the artwork into `seed/art/` |
| [pages/](pages/) | Site page sections and `pages.json` (title, route, template) |
| [menus/](menus/) | Main and footer menu items |
| [shots.json](shots.json) | The screenshot list for `scripts/capture-screenshots.py` |
| [walkthrough.json](walkthrough.json) | The shot list for [`scripts/make-walkthrough.py`](../scripts/make-walkthrough.md) |

## Notes

- Lantern Ramblers, its members, the venues, festivals and photographers are fictional. The cities are real.
  Ticket, video and recording links point at `example.com`, and email addresses use `example.com`.
- It's a fan tribute: the site describes the band as a Grateful Dead tribute and uses song titles in setlists, but
  no Grateful Dead logos, artwork or imagery. The posters and portraits are abstract artwork drawn by
  [seed/make-art.py](seed/make-art.py), so every image is license-free and no real people appear.
- Ticket prices are shown for information only. Tickets are sold by each venue, and there are no payment forms.
- The booking endpoint is public by design. Spam protection is the honeypot plus server-side checks, and nothing is
  published. Add rate limiting at your proxy if you expect heavy traffic.
- The setlist links on the tour page assume a show and its setlist have the same title, which is how the seed and the
  admin labels set them up.
- Motion (the drifting colour, the turning logo, the ticker and the chart bars) stops when the visitor asks for
  reduced motion.
- Fonts: Fraunces for headlines, Instrument Sans for text and DM Mono for labels, from Google Fonts. Bootstrap Icons
  load from jsDelivr.
- A fresh install also has an About page and a `posts` content type. The build leaves them alone; delete them if you
  don't need them.
