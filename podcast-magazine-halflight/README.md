# Halflight: a podcast and magazine website

The website for Halflight (fictional), an independent publisher with a weekly podcast and a quarterly print magazine about people who work the night shift, built on Raytha. The home page leads with the latest episode (player, waveform, chapters count) next to a 24-hour "night clock" that draws every guest's shift as an arc with a hand at the current time, worked out on the server. Below it: the next episode with a countdown, the current print issue with its contents page, the season's running order with each shift on a 24-hour bar, and listener letters stamped with the time they were written. Members sign in to a back room with bonus episodes, the archive and the next issue early; editors get a production board. "Night clock and contents page" design, with no payment, subscription, registration or sign-up forms. The kit suits a podcast or magazine publisher that wants to run its own site, or an agency building one for a client.

- **Brief:** [brief.md](brief.md)
- **Build time:** under an hour
- **Write-up:** [raytha.com/use-cases/halflight-magazine](https://raytha.com/use-cases/halflight-magazine)
- **Walkthrough:** [MP4](https://raytha.com/raytha/media-items/objectkey/MafyEFgnzU6C-jWgmYdqfA_halflight_magazine_walkthrough.mp4)

![Halflight home](https://raytha.com/raytha/media-items/objectkey/--taRjukQUiJ8vA84cJjrg_halflight_01_home.webp)

## Rebuild

```bash
RAYTHA_URL=https://your-site.example RAYTHA_API_KEY=... bash build.sh
```

6 content types (episodes, issues, stories, contributors, letters, rundown items), 2 user groups (`members`, `editors`), site pages (home, hour index, about, members back room, editors desk, search), menus. Server-rendered Liquid only. `build.sh` runs `../scripts/build-example.sh`.

**Audio.** Each episode has an `audio_url` field; when it is set, the episode page, the home page and the back room render a native `<audio>` player. The seed leaves it empty. Upload your MP3s to the media library (or point at your podcast host's file URLs) and set `audio_url` on each episode. The published screenshots use one short sample clip for every episode.

## How the pages work

- **The clock.** Templates read `"now" | date` in the site's time zone (Settings in the admin; the example uses America/Chicago) for the hour, the quarter hour and today's date.
- **The night clock.** An inline SVG. A lookup table of unit vectors for all 96 quarter hours (midnight at the top) turns each episode's `shift_start` and `shift_end` hours into an arc on its own ring, with the large-arc flag set for shifts over 12 hours and overnight shifts wrapping past midnight. Guests on shift now (start/end compared with the current hour, including overnight shifts) get a thicker arc and an "on shift" tag. The same table draws the hand on each magazine cover from `cover_hour`.
- **Release dates.** Episodes store `release` as `YYYY-MM-DD`. Lists and the dial compare it with today as `YYYYMMDD` numbers, so a future episode shows as "coming in N days" and keeps its notes and transcript back until the date, with no republishing.
- **Issues and contents pages.** Stories store an issue number, section, page, reading time and audience. The issue page builds its contents page from the stories filed under it, sorted by page, and lists the episodes that share the issue number.
- **The hour index.** `/hours?h=N` (default: the current hour) lists episodes whose shift covers that hour, stories set at it and letters written at it. Hours are plain links; no JavaScript.
- **Waveforms** are drawn from a comma-separated list of bar heights stored on each episode; chapters are `mm:ss Title` entries separated by `|`.
- Numeric field values are captured into strings and converted with `plus: 0` before they are compared or used in math, and date fields are captured before the `date` filter.
- Search runs `get_content_items` with an OData `contains(...)` filter across episodes, stories, issues, people and letters, and shows only the titles of members-only items to visitors who are not signed in.

## Members-only areas

- User groups `members` and `editors` (editors also count as members; admins see everything). Gating is server-side in Liquid with `CurrentUser.UserGroups`.
- Episodes and stories have an `audience` field (public, members, editors). Detail templates render the content or a lock panel; lists, contents pages and search show members-only titles with a lock and no contents; the HTML meta description falls back to a generic line for members-only items.
- `/members`: bonus episodes with players, the next issue's early stories and the archive by issue; signed out, titles only. `/desk`, `/rundown` and rundown pages are editors-only: items due this week, past due, days until the next episode, and a board from booked to live.
- No sign-up form: create users in the admin and add them to a group. Demo passwords are not stored in this repository.

## Screenshots and walkthrough

[screenshots/](screenshots/README.md) lists the published screenshots. `shots.json` and `walkthrough.json` are the shot lists used to capture them (see [../scripts/make-walkthrough.md](../scripts/make-walkthrough.md)); signed-in shots read the demo login from `SITE_USER_EMAIL` and `SITE_USER_PASSWORD`.
