# Harlow Creek Health System: a self-hosted hospital / health system website

The public website of Harlow Creek Health System, a fictional regional health system, built on Raytha 2.0.1 by an
AI agent with the [`raytha` CLI](https://github.com/RaythaHQ/raytha-cli). Find a doctor with specialty filters, locations
and facilities, departments and services, patient and visitor information, health news, careers, events and classes, and
a staff-only portal for clinician resources. Every template, content type, item, page, menu and user group went in through
the CLI. Nobody opened the admin.

- **Brief:** [brief.md](brief.md)
- **Build time:** under an hour of agent time, from an empty install to `raytha check` passing
- **Write-up:** [raytha.com/use-cases/harlow-creek-health-system](https://raytha.com/use-cases/harlow-creek-health-system)
- **Walkthrough video:** [MP4, 36 s](https://raytha.com/raytha/media-items/objectkey/gTYZJX9CrkuvB6OMbkb7bw_harlow_creek_walkthrough.mp4) (shot list: [walkthrough.json](walkthrough.json))

![Harlow Creek Health System home page](https://raytha.com/raytha/media-items/objectkey/_djXRHTtwkmAnyYZ0iLF6w_harlow_01_home.webp)

## Screenshots

| | |
|---|---|
| ![Find a doctor](https://raytha.com/raytha/media-items/objectkey/uCYA4xjbZUOX5Gnw2IrSYw_harlow_03_providers.webp) | ![Locations](https://raytha.com/raytha/media-items/objectkey/Sgwgs31QoUmOwN2C9kKAQA_harlow_07_locations.webp) |
| Find a doctor, with specialty filters and accepting-patient flags | Hospital, urgent care, clinics and specialty centers |
| ![Services](https://raytha.com/raytha/media-items/objectkey/isF7p86gIEmSEjqN8Fju3w_harlow_05_services.webp) | ![Staff portal](https://raytha.com/raytha/media-items/objectkey/vavyEsTEGkOzSJS3I0Ef3A_harlow_16_staff.webp) |
| Departments and specialty service lines | The staff portal, signed in, with clinician resources |

<p>
  <img src="https://raytha.com/raytha/media-items/objectkey/nLzd1ZRJUEOMEh-3mop4uQ_harlow_22_home_mobile.webp" width="240" alt="Home page on a phone">
  <img src="https://raytha.com/raytha/media-items/objectkey/Tguvmp6t30ezu4xk0chMSw_harlow_24_providers_mobile.webp" width="240" alt="Find a doctor on a phone">
  <img src="https://raytha.com/raytha/media-items/objectkey/QqDl8f-et0udb-Kl62nV5Q_harlow_25_locations_mobile.webp" width="240" alt="Locations on a phone">
</p>

More in [screenshots/](screenshots/). Recapture them from your own build with [shots.json](shots.json) and
[`scripts/capture-screenshots.py`](../scripts/capture-screenshots.py) (the staff portal shots need a signed-in staff user:
set `SITE_USER_EMAIL` and `SITE_USER_PASSWORD`).

## What's in it

- A **home page** at `/`: find-a-doctor search, quick tasks, featured departments, upcoming classes, news and locations.
- **Find a doctor** at `/providers`, filterable by specialty and accepting new patients (`?specialty=` and `?accepting=true`).
  Each provider page has credentials, languages, telehealth and accepting flags, and links to location and department.
- **Services** at `/services`, filterable by category, with relationship fields to locations.
- **Locations** at `/locations`: hospital, urgent care, clinic and specialty centers, each with hours, parking and services.
- **Patient and visitor info** at `/resources` and `/patients`.
- **News** at `/news`, **events and classes** at `/events`, **careers** at `/careers`.
- A **staff portal** at `/staff` and staff-only resources, for members of the `staff` user group.
- **About**, **contact**, **accessibility** and **search** at `/search?q=...`.

## How find a doctor and the staff portal work

- Each provider is an item with specialty, location and department relationship fields, plus accepting and telehealth
  checkboxes. The directory and search read the same items with `get_content_items`.
- [hc_staff.liquid](theme/web-templates/hc_staff.liquid) and
  [hc_detail_resources.liquid](theme/web-templates/hc_detail_resources.liquid) loop over `CurrentUser.UserGroups`. Staff
  (and admins) see the resources; everyone else sees a sign-in prompt.

## Rebuild it

```bash
# From a Raytha 2.x install with RAYTHA_URL and RAYTHA_API_KEY set:
bash build.sh
```

`build.sh` generates seed art if needed, then runs [`scripts/build-example.sh`](../scripts/build-example.sh), which
imports the schema, pushes the theme, seeds content, creates the `staff` user group, the site pages and menus, then runs
`raytha check`.

To see the staff portal, create a public user in the admin, add them to `staff`, and sign in at `/account/login`.

## Notes

- Harlow Creek Health System is fictional. Nothing here is medical advice, and no real patient data appears.
- The staff sign-in is a Raytha website account, not the electronic health record.
- There are no payment or registration forms on this site.

## Layout of this folder

| Path | Purpose |
|------|---------|
| [schema.json](schema.json) | Content types, fields, choices and views (`raytha schema import`) |
| [theme/](theme/) | Liquid web and widget templates |
| [seed/](seed/) | JSONL content plus `make-art.py` (generated SVGs/PDFs are gitignored) |
| [pages/](pages/) | Site pages and widget sections |
| [menus/](menus/) | Main and footer menus |
| [shots.json](shots.json) / [walkthrough.json](walkthrough.json) | Screenshot and video shot lists |
| [example.json](example.json) | Theme name, content type order, detail templates, user groups |
| [build.sh](build.sh) | One-command rebuild |
