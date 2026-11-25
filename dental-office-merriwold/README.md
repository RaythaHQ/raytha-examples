# Merriwold Dental: a dental office website

The website for Merriwold Dental (fictional), an independent family dental practice in the fictional town of Tansey Ford, built on Raytha. The site starts from the mouth: a chart of all 32 adult teeth in Universal numbering, drawn as an SVG on the server, where every tooth is a link to the treatments used on it. Fifteen treatments carry their visits with chair minutes for each, an honest 1-5 "how it feels" rating, numbing, recovery and the matching aftercare sheet. Aftercare guides show an hour-by-hour recovery timeline; answers, chairside notes and the team round it out. Patients sign in to a patient room with aftercare, home care and printable forms; the team gets a morning huddle board. "Left rail and tooth map" design, with no booking, registration, sign-up or payment forms and no patient records. The kit suits a dental practice that wants to own its site, or an agency or freelancer building one for a dental client.

- **Brief:** [brief.md](brief.md)
- **Build time:** under an hour
- **Write-up:** [raytha.com/use-cases/merriwold-dental](https://raytha.com/use-cases/merriwold-dental)
- **Walkthrough:** [MP4](https://raytha.com/raytha/media-items/objectkey/an5zVTDQ7UGMPhaA648vuA_merriwold_dental_walkthrough.mp4)

![Merriwold Dental home](https://raytha.com/raytha/media-items/objectkey/iidM3v75BkGVLPoWL1JAIA_merriwold_01_home.webp)

## Rebuild

```bash
RAYTHA_URL=https://your-site.example RAYTHA_API_KEY=... bash build.sh
```

6 content types (treatments, team, guides, answers, chairside notes, huddle items), 2 user groups (`patients`, `team`), site pages (home, tooth map, first visit, patient room, team huddle, search), menus. Server-rendered Liquid only. `build.sh` runs `../scripts/build-example.sh`.

## How the pages work

- **Teeth as data.** Treatments, answers and team members store Universal tooth numbers as a comma-separated `teeth` field; chairside notes store a single `tooth`. Templates wrap the list in commas and test `contains ",N,"`.
- **The chart.** One inline SVG generated with the position and angle of each tooth along two arches. Each tooth is a link to `/chart?t=N` with a class set in Liquid: `hl` when its number is in the page's highlight list, `sel` when it is the selected tooth. The same chart, smaller, shows where a treatment is used, which teeth a clinician works on, and the tooth a note is about.
- **The tooth map page.** `/chart?t=N` shows the tooth's name, age it comes in, roots and job (lookup arrays in the template), every treatment whose `teeth` contains N with visits, chair time and feel, and the answers and notes about it, with previous/next tooth links. `/chart?f=family` collects the teeth of every treatment in that family and highlights them.
- **Visits and timelines.** `visits` is stored as `minutes~what happens` entries separated by `|`; templates split it for the visit cards, the chair-time bars and the totals. Aftercare `timeline` is `hours~what to expect` entries, drawn as a recovery track labeled "2 hours", "Day 3", "Week 1".
- **Open now and today.** The sidebar's open/closed chip and the highlighted row in the hours table come from `"now" | date` in the site's time zone (the example uses America/Chicago). The team huddle compares each item's `YYYY-MM-DD` date with today as a `YYYYMMDD` number.
- Numeric field values are captured into strings and converted with `plus: 0` before they are compared or used in math.
- Search runs `get_content_items` with an OData `contains(...)` filter across treatments, answers, guides, notes and the team, and shows only the titles of patient-only sheets to visitors who are not signed in.

## Members-only areas

- User groups `patients` and `team` (team members also count as patients; admins see everything). Gating is server-side in Liquid with `CurrentUser.UserGroups`.
- Guides and huddle items have an `audience` field (public, patients, team). Detail templates render the content or a lock panel; the library, the patient room and search show patient-only titles with a lock and no contents; the HTML meta description falls back to a generic line for those pages.
- `/patients`: aftercare, home care and printable forms grouped by kind; signed out, titles only. `/desk`, `/huddle` and huddle pages are team-only: today and carried over, coming up, and done.
- The printable forms are fictional samples to print at home; nothing is submitted through the site and no patient data is stored.
- No sign-up form: create users in the admin and add them to a group. Demo passwords are not stored in this repository.

## Screenshots and walkthrough

[screenshots/](screenshots/README.md) lists the published screenshots. `shots.json` and `walkthrough.json` are the shot lists used to capture them (see [../scripts/make-walkthrough.md](../scripts/make-walkthrough.md)); signed-in shots read the demo login from `SITE_USER_EMAIL` and `SITE_USER_PASSWORD`.
