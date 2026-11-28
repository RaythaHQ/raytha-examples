# Wyndleford Parish Church: a church website

The website for Wyndleford Parish Church (fictional), a parish on the green in the fictional town of Wyndleford, built on Raytha. The site keeps time by the church year: a ribbon across the top of every page shows Advent 2026 to Advent 2027 with each season sized by its days and today marked, and the page's accent color comes from the season that contains today. The home page opens like a Sunday bulletin with the Sunday's name, color, service times, lectionary readings, hymns and preacher, then the next seven days from the calendar. The church year is also drawn as an SVG wheel where every season is a link that previews the whole site in its colors. Sundays and sermons are grouped by season, the calendar is a month grid with each day's season and every Sunday's name, and ministries, small groups and clergy and staff round it out. Members sign in for the parish directory, the full prayer list, the volunteer rota and small group hosts; some prayer requests stay with the clergy. "Bulletin and ribbon" design, with no giving, registration, sign-up or payment forms. The kit suits a church that wants to own its site, or an agency or freelancer building one for a church client.

- **Brief:** [brief.md](brief.md)
- **Build time:** under an hour
- **Write-up:** [raytha.com/use-cases/wyndleford-parish-church](https://raytha.com/use-cases/wyndleford-parish-church)
- **Walkthrough:** [MP4](https://raytha.com/raytha/media-items/objectkey/NqYWLpm2eUWg2TJT1m61gA_wyndleford_parish_church_walkthrough.mp4)

![Wyndleford Parish Church home](https://raytha.com/raytha/media-items/objectkey/tDRBcNX9zUWLaUe4Lf6vBg_wyndleford_01_home.webp)

## Rebuild

```bash
RAYTHA_URL=https://your-site.example RAYTHA_API_KEY=... bash build.sh
```

9 content types (Sundays, seasons, calendar events, ministries, small groups, people, directory households, prayer requests, rota slots), 2 user groups (`members`, `clergy`), site pages (home, plan a visit, members, search), menus. Server-rendered Liquid only. `build.sh` runs `../scripts/build-example.sh`, then tidies routes made from titles with punctuation (for example `The Rev. Miriam Achterberg`).

## How the pages work

- **Seasons as data.** Each season stores `start` and `end` dates, a liturgical color and two hex colors (`hex`, `tint`). The base layout loops over the seasons, finds the one whose dates contain today (compared as `YYYYMMDD` numbers), and writes its colors into the `--acc` and `--tint` CSS variables. `?s=lent` on any page, or opening a season's own page, previews another season.
- **The ribbon.** A row of links, one per season, with `flex-grow` set to the season's number of days (from `date: "%s"` arithmetic) and a marker at today's position in the year.
- **The wheel.** One SVG `<circle>` per season with `pathLength` set to the number of days in the church year, so `stroke-dasharray` is the season's days and `stroke-dashoffset` its offset from Advent. Labels sit on a circular `textPath` (a reversed path for the lower half so they read the right way up), and a needle is rotated to today.
- **The bulletin.** The home page finds the next Sunday on or after today. `readings` is stored as `reference~label` entries and `hymns` as `number~title~place` entries separated by `|`; templates split them into the order of service.
- **The week strip and the calendar.** Days are built from Unix timestamps (`now` plus `i` times 86400) and formatted with `date`. `/calendar?m=YYYY-MM` works out the weekday of the first, the number of days in the month, and for every cell its season color, the Sunday's name and the events on that date.
- Numeric field values are captured into strings and converted with `plus: 0`, and date fields are captured before `date` formatting, so comparisons and math work on plain values.
- Search runs `get_content_items` with an OData `contains(...)` filter across Sundays, events, ministries, small groups, people and seasons.

## Members-only areas

- User groups `members` and `clergy` (clergy also count as members; admins see everything). Gating is server-side in Liquid with `CurrentUser.UserGroups`.
- Directory households, prayer requests, rota slots and some events have an `audience` field (public, members, clergy). Detail templates render the content or a lock panel; list pages render a lock panel for visitors who are not signed in; the HTML meta description falls back to a generic line for those pages.
- `/prayer`: requests that are read aloud are shown to everyone; members-only and clergy-only requests are left out on the server and only counted.
- `/members`: household and prayer counts, the member's next rota slot, this Sunday's rota and every group's host and address. `/rota`: six Sundays by eight roles, the signed-in member's slots highlighted, swaps wanted. `/directory`: households by neighborhood.
- No sign-up form: create users in the admin and add them to a group. Demo passwords are not stored in this repository. All names, phone numbers and emails are fictional.

## Screenshots and walkthrough

[screenshots/](screenshots/README.md) lists the published screenshots. `shots.json` and `walkthrough.json` are the shot lists used to capture them (see [../scripts/make-walkthrough.md](../scripts/make-walkthrough.md)); signed-in shots read the demo login from `SITE_USER_EMAIL` and `SITE_USER_PASSWORD`.
