# Larkmoor College: a self-hosted college website

The public website of Larkmoor College, a fictional liberal arts and sciences college, built on Raytha 2.0.1 by an
AI agent with the [`raytha` CLI](https://github.com/RaythaHQ/raytha-cli). A program finder across six schools, a faculty
directory, admissions with deadlines and visits, an illustrated campus map, news, events, athletics schedules and a
members-only portal for students, faculty and staff. Every template, content type, item, page, menu and user group went in
through the CLI. Nobody opened the admin.

- **Brief:** [brief.md](brief.md)
- **Build time:** under an hour of agent time, from an empty install to `raytha check` passing
- **Write-up:** [raytha.com/use-cases/larkmoor-college](https://raytha.com/use-cases/larkmoor-college)
- **Walkthrough video:** [MP4, 36 s](https://raytha.com/raytha/media-items/objectkey/yIb_ZLmDpECs1zmTO4Y9Cw_larkmoor_college_walkthrough.mp4) (shot list: [walkthrough.json](walkthrough.json))

![Larkmoor College home page](https://raytha.com/raytha/media-items/objectkey/u4M9p7zqK0aVyP9h0FPlxA_larkmoor_01_home.webp)

## Screenshots

| | |
|---|---|
| ![Programs](https://raytha.com/raytha/media-items/objectkey/w-sh3zwFSkKh01EAnbCePg_larkmoor_03_programs.webp) | ![Campus map](https://raytha.com/raytha/media-items/objectkey/8p51bEuzHU2GPsxKOxg9qQ_larkmoor_08_campus.webp) |
| Programs across six schools, filtered by school and degree | Campus life with an illustrated map |
| ![Faculty directory](https://raytha.com/raytha/media-items/objectkey/8Q1uTz17E0GzpKQjhdvY6w_larkmoor_06_faculty.webp) | ![Portal](https://raytha.com/raytha/media-items/objectkey/razFieGBS0CxShJwV96Qig_larkmoor_27_portal_faculty.webp) |
| The faculty directory | The portal, signed in as faculty |

<p>
  <img src="https://raytha.com/raytha/media-items/objectkey/dtFWi0c70kqyr7fsT8rb2Q_larkmoor_23_home_mobile.webp" width="240" alt="Home page on a phone">
  <img src="https://raytha.com/raytha/media-items/objectkey/3bj7n4WXaEODyuXu2YVxYA_larkmoor_25_programs_mobile.webp" width="240" alt="Programs on a phone">
  <img src="https://raytha.com/raytha/media-items/objectkey/eOc-E_PVG0-b31y93FpXbQ_larkmoor_26_campus_mobile.webp" width="240" alt="Campus map on a phone">
</p>

More in [screenshots/](screenshots/). Recapture them from your own build with [shots.json](shots.json) and
[`scripts/capture-screenshots.py`](../scripts/capture-screenshots.py) (the portal shots need a signed-in member of the
`students` or `faculty` group: set `SITE_USER_EMAIL` and `SITE_USER_PASSWORD`).

## What's in it

- A **home page** at `/`: a program finder, quick links, the six schools, featured programs, events, news, the campus map and athletics.
- **Programs** at `/programs`, filterable by school, degree and keyword (`?school=`, `?degree=`, `?q=`). Each program page
  lists courses, outcomes, faculty in the program and the building it is based in.
- A **faculty directory** at `/faculty`, searchable by name, school and interest.
- **Campus life** at `/campus` with an illustrated map and a page per building, showing the events and programs there.
- **Admissions** at `/admissions`: how to apply, deadlines, cost and aid, visits and an FAQ. No application forms.
- **News** at `/news`, **events** at `/events`, **athletics** at `/athletics` with schedules and results per team.
- A **student and faculty portal** at `/portal` and members-only resources, for the `students` and `faculty` user groups.
- **About**, **contact**, **accessibility** and **search** at `/search?q=...`.

## How the directory and the portal work

- Each faculty profile relates to a program, and each program to a building, so pages link to each other without
  duplicated data. Listings and search read the same items with `get_content_items`.
- [lm_portal.liquid](theme/web-templates/lm_portal.liquid) and
  [lm_detail_resources.liquid](theme/web-templates/lm_detail_resources.liquid) loop over `CurrentUser.UserGroups`.
  Students see student resources; faculty (and admins) also see faculty resources; everyone else sees a sign-in prompt.
- Widget templates read their settings from `widget.settings`.

## Rebuild it

```bash
# From a Raytha 2.x install with RAYTHA_URL and RAYTHA_API_KEY set:
bash build.sh
```

`build.sh` generates seed art if needed, then runs [`scripts/build-example.sh`](../scripts/build-example.sh), which
imports the schema, pushes the theme, seeds content, creates the `students` and `faculty` user groups, the site pages and
menus, then runs `raytha check`.

To see the portal, create a public user in the admin, add them to `students` or `faculty`, and sign in at `/account/login`.

## Notes

- Larkmoor College is fictional. Its students, faculty, buildings, teams and documents are invented.
- The portal sign-in is a Raytha website account, not a student information system or learning management system.
- There are no application, registration or payment forms on this site.

## Layout of this folder

| Path | Purpose |
|------|---------|
| [schema.json](schema.json) | Content types, fields, choices and views (`raytha schema import`) |
| [theme/](theme/) | Liquid web and widget templates |
| [seed/](seed/) | JSONL content plus `make-art.py` (generated images and PDFs are gitignored) |
| [pages/](pages/) | Site pages and widget sections |
| [menus/](menus/) | Main and footer menus |
| [shots.json](shots.json) / [walkthrough.json](walkthrough.json) | Screenshot and video shot lists |
| [example.json](example.json) | Theme name, content type order, detail templates, user groups |
| [build.sh](build.sh) | One-command rebuild |
