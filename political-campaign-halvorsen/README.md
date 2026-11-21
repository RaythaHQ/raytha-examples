# Noor Halvorsen for County Commission: a political campaign website

The website for Noor Halvorsen (fictional), a candidate for a nonpartisan county commission seat in fictional Wrenfield County, built on Raytha. The home page leads with the candidate's yard sign and a countdown to Election Day worked out on the server, then a "road to April 6" rail of key dates, the plan laid out like a sample ballot (each item with what will be done, what it costs and how voters will know it worked), a precinct map whose outlines and polling places come from content, upcoming events split into today and coming up, questionnaire answers in full, and endorsements. Volunteers and staff sign in to members-only desks. "Yard sign and sample ballot" design, with no donation, payment, registration or sign-up forms, and no party named or implied. The kit suits a campaign that wants to run its own site, or a consultant, agency or freelancer building candidate sites for clients.

- **Brief:** [brief.md](brief.md)
- **Build time:** under an hour
- **Write-up:** [raytha.com/use-cases/halvorsen-for-wrenfield](https://raytha.com/use-cases/halvorsen-for-wrenfield)
- **Walkthrough:** [MP4](https://raytha.com/raytha/media-items/objectkey/xWLGSPq93UCeEqt7S5kOJg_halvorsen_for_wrenfield_walkthrough.mp4)

![Noor Halvorsen for County Commission home](https://raytha.com/raytha/media-items/objectkey/MFvgBe8Va0S0e0mdvPTCTQ_halvorsen_01_home.webp)

## Rebuild

```bash
RAYTHA_URL=https://your-site.example RAYTHA_API_KEY=... bash build.sh
```

8 content types (plan items, precincts, events, endorsements, questionnaire answers, milestones, notes, volunteer shifts), 2 user groups (`volunteers`, `staff`), site pages (home, district map, how to vote, Meet Noor, Help out, volunteer desk, staff desk, search), menus. Server-rendered Liquid only. `build.sh` runs `../scripts/build-example.sh`.

## How the pages work

- **The clock.** The base layout reads `"now" | date` in the site's time zone and converts stored `YYYY-MM-DD` dates to day counts with `date: "%s"`. Set the time zone in the admin (Settings); the example was built with America/Chicago.
- **Countdown and road.** Milestones are content. The layout finds Election Day, early voting and the registration deadline by label, and the top strip and the hero card count down to them. The home page rail spaces milestones evenly and places a "today" marker between the last date passed and the next one, in proportion to the days in between.
- **The plan as a sample ballot.** Plan items carry a ballot number, a one-line stance, pipe-separated commitments and measures, and a cost note. The item page renders three boxes and links to the previous and next ballot item by number.
- **The district map.** An inline SVG. Each precinct stores its outline as SVG path data, a label position and a polling-place position. The public map colors and numbers the precincts; `/vote?p=N` and each precinct page highlight one precinct. The volunteer desk draws the same outlines shaded by doors knocked against the door goal.
- **Events** are split on the server into today, coming up and already happened by comparing `YYYYMMDD` numbers. Volunteer-only events show with a lock.
- **Answers** can be filtered by topic with `?topic=`, built from the topics present in the content.
- Numeric field values are captured into strings and converted with `plus: 0` before they are compared or used in math, because decimal field values are not directly numeric in Liquid.
- Search runs `get_content_items` with an OData `contains(...)` filter across the public types and hides the contents of members-only notes.

## Members-only areas

- User groups `volunteers` and `staff` (staff also count as volunteers; admins see everything). Gating is server-side in Liquid with `CurrentUser.UserGroups`.
- Notes and events have an `audience` field (public, volunteers, staff). Detail templates render the content or a lock panel; lists and search show members-only titles with a lock and no contents; the HTML meta description falls back to a generic line for members-only items.
- `/volunteers`: next shifts with open spots, the shaded turf map, briefs and the door script. `/staff`: days to Election Day and the registration deadline, district door totals, a precinct table flagging precincts behind 40 percent, and staff memos. `/shifts` and shift pages are volunteers-only.
- Precinct pages show canvass progress and the precinct captain only to volunteers and staff.
- No sign-up form: create demo users in the admin and add them to a group. Demo passwords are not stored in this repository.

## Screenshots and walkthrough

[screenshots/](screenshots/README.md) lists the published screenshots. `shots.json` and `walkthrough.json` are the shot lists used to capture them (see [../scripts/make-walkthrough.md](../scripts/make-walkthrough.md)); signed-in shots read the demo login from `SITE_USER_EMAIL` and `SITE_USER_PASSWORD`.
