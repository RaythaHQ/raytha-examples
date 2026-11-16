# Cadwallow Park: a city park website

The website for Cadwallow Park (fictional), a 410-acre city park run by a parks and recreation department, built on Raytha. The home page is built like a trailhead kiosk: an illustrated park map whose trail lines and numbered places come from content, next to a "today at the park" panel with the gates, approximate sunrise and sunset, and how many places are open right now, all worked out on the server. Every gate, playground, shelter, field, garden and restroom shows whether it is open now from its stored hours and season. Five blazed trails have elevation profiles drawn on the server, the tree register has numbered tags and a map layer, "look for" picks this month's sightings on its own, and there are a conditions board and park projects with phase trackers. A stewards' shed for the Friends of the park and a crew board for park staff are gated on the server. "Trailhead kiosk" design, with no booking, payment, registration or sign-up forms. The kit suits a city or county parks department, the city IT team that hosts it, or an agency building parks and recreation sites.

- **Brief:** [brief.md](brief.md)
- **Build time:** under an hour
- **Write-up:** [raytha.com/use-cases/cadwallow-park](https://raytha.com/use-cases/cadwallow-park)
- **Walkthrough:** [MP4](https://raytha.com/raytha/media-items/objectkey/iOFAtY0XQE63AEOMwptWjg_cadwallow_park_walkthrough.mp4)

![Cadwallow Park home](https://raytha.com/raytha/media-items/objectkey/JkdPuPWWMUC7Jibd-GYHnA_cadwallow_01_home.webp)

## Rebuild

```bash
RAYTHA_URL=https://your-site.example RAYTHA_API_KEY=... bash build.sh
```

8 content types (places, trails, trees, sightings, conditions, projects, events, bulletins), 2 user groups (`friends`, `staff`), site pages (home, park map, plan a visit, shelters and fields, about, stewards' shed, crew board, search), menus. Server-rendered Liquid only. `build.sh` generates the place illustrations if `seed/art` is missing, then runs `../scripts/build-example.sh`.

## How the pages work

- **The clock.** Every template starts from `"now" | date` (month, day, hour and minute in the site's time zone). Gates are open from 5:00 am to 11:00 pm. Sunrise and sunset come from a twelve-entry table of mid-month times, interpolated by the day of the month; dusk is the day's sunset. Approximate, and labeled so.
- **Open now.** Each place stores `open_min` and `close_min` (minutes after midnight), a closing rule (`fixed` or `dusk`) and `season_from`/`season_to` months (0 = all year; a season like December to February wraps the new year). The template works out open, closing soon (within an hour), opens later, closed now or out of season, and the hours it opens or closes. `/places` filters by kind and by `?open=now` on the server.
- **The park map.** An inline SVG: the ground (woods, meadow, the Wallow, creek, contours, streets) is drawn in the template; each trail's line is its `path` field (SVG path data) stroked in its `blaze_color`; each place is a numbered marker at its `x`/`y` fields; trees can be added as a layer with `?layer=trees`. Detail pages reuse the map with one trail highlighted or one place ringed.
- **Trails** store length, climb, surface, access, a blaze shape and color, an elevation `profile` (comma-separated feet) and `waypoints` (`mile~note|…`). Profiles are SVG polylines computed in Liquid on one shared vertical scale, as sparklines in lists and full size on trail pages. Each trail page lists the conditions whose `applies_to` matches the trail.
- **Look for** entries store the months they can be seen (`Oct|Nov|…`). The home page filters with an OData `contains(months,'Nov')` for the current month; `/look-for` takes `?month=` and draws a year chart.
- **Trees** show a trunk cross-section drawn from the girth (girth ÷ π). **Projects** draw a five-step phase tracker and a funded-versus-budget bar from stored numbers.
- Search runs `get_content_items` with an OData `contains(...)` filter across eight content types, and hides the contents of Friends- and staff-only items from browsers that should not see them.

## Members-only areas

- Events and bulletins have an `audience` field (`public`, `friends`, `staff`; bulletins are always one of the two groups).
- Templates read `CurrentUser.UserGroups` on the server and render either the content or a lock panel with a sign-in link. Admins see everything. Lists show members-only titles with a lock and leave their contents out; the page description in the HTML head uses a generic line for members-only items.
- `/stewards` (template `cp_stewards`) shows a steward badge with the next workday, today's sunset and daylight, workdays, plans, tool shed notes, minutes and adopted plots, only for the `friends` group.
- `/crew` (template `cp_crew`) shows a crew badge with tonight's lock-up and dusk, the live status of every place, work orders, the rota and closure plans, everything closed or under caution, staff events and this week's assignments, only for the `staff` group. Each area points a signed-in member of the other group back to their own.
- To try it, create a public user in the admin, add them to `friends` and/or `staff`, and sign in at `/account/login`. There is no registration form on purpose.

## Notes

- Place illustrations (`seed/art/*.svg`) are generated by `seed/make-art.py`; `build.sh` runs it when the folder is missing. No real park, person or tree is pictured.
- Set the site's time zone in the admin (Settings) so "open now" matches local time; the example was built with America/Chicago.
- Dropdown values are rendered as their developer names and mapped to labels in the templates with `case`.
- Number fields are converted with `append: "" | plus: 0` before arithmetic; field values are captured into strings before they are compared.
- Web template includes are not used; shared pieces are inlined in each template.
- Everything is fictional: the park, its city, people, trees, projects and figures. Phone numbers use the 555 range.

## Files

| Path | What it is |
|---|---|
| [brief.md](brief.md) | The brief |
| [example.json](example.json) | Theme name, content type order, detail templates, user groups |
| [schema.json](schema.json) | Content types, fields and views |
| [theme/](theme/) | Web templates (`cp_*`, login and 404) and widget templates |
| [seed/](seed/) | Seed content (JSONL) and the art generator |
| [pages/](pages/) | Site pages and their widget sections |
| [menus/](menus/) | Main and footer menus |
| [shots.json](shots.json) | Screenshot list |
| [walkthrough.json](walkthrough.json) | Walkthrough video shot list (`../scripts/make-walkthrough.py`) |
| [screenshots/](screenshots/) | Screenshots |
