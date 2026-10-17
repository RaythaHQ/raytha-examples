# Halverline Studio: a web design agency site with a client portal

The website of Halverline Studio, a fictional web design and development studio, built on Raytha 2.0.1 by an
AI agent with the [`raytha` CLI](https://github.com/RaythaHQ/raytha-cli). Case studies, services, a team page,
insights, careers, client logos and testimonials, and a members-only client portal with project rooms, weekly updates,
deliverables and brand assets. Every template, content type, item, page, menu and user group went in through the CLI.
Nobody opened the admin.

- **Brief:** [brief.md](brief.md)
- **Build time:** under an hour of agent time, from an empty install to `raytha check` passing
- **Write-up:** [raytha.com/use-cases/halverline-studio](https://raytha.com/use-cases/halverline-studio)
- **Walkthrough video:** [MP4, 35 s](https://raytha.com/raytha/media-items/objectkey/b2S7qqlYiU2DbotjkCS1pw_halverline_studio_walkthrough.mp4) (shot list: [walkthrough.json](walkthrough.json))

![Halverline Studio home page](https://raytha.com/raytha/media-items/objectkey/JuspflfzjEO9Wrr5VSdVpQ_halverline_01_home.webp)

## Screenshots

| | |
|---|---|
| ![Case studies](https://raytha.com/raytha/media-items/objectkey/OsVuUOWcx0KV2wP7ADqaUw_halverline_03_work.webp) | ![A case study](https://raytha.com/raytha/media-items/objectkey/D_yQrpPb0EKX_W3wpeSs_g_halverline_06_case_study_top.webp) |
| Case studies, filterable by industry | A case study |
| ![Client portal](https://raytha.com/raytha/media-items/objectkey/QGo-j4ZeGEW9kxBSWN4BKw_halverline_19_portal_client.webp) | ![Project room](https://raytha.com/raytha/media-items/objectkey/JDNa4p7aA0GOuPGZN4-7JA_halverline_20_project_room.webp) |
| The client portal, signed in as a client | A project room with updates and files |

<p>
  <img src="https://raytha.com/raytha/media-items/objectkey/f7emLbQFlU-Vt9yDpVw2Qg_halverline_26_home_mobile.webp" width="240" alt="Home page on a phone">
  <img src="https://raytha.com/raytha/media-items/objectkey/PMLzXrDnj0iR8W6EtY3wqw_halverline_28_case_study_mobile.webp" width="240" alt="A case study on a phone">
  <img src="https://raytha.com/raytha/media-items/objectkey/UPlzPmTBL0qOJbBYvK0ZYQ_halverline_29_portal_client_mobile.webp" width="240" alt="Client portal on a phone">
</p>

More in [screenshots/](screenshots/). Recapture them from your own build with [shots.json](shots.json) and
[`scripts/capture-screenshots.py`](../scripts/capture-screenshots.py) (the portal shots need a signed-in member of a
`client_` group or `studio`: set `SITE_USER_EMAIL` and `SITE_USER_PASSWORD`).

## What's in it

- A **home page** at `/`: selected work, a client logo wall, services, the process, a testimonial and recent insights.
- **Case studies** at `/work`, filterable by industry (`?industry=`). Each one has the challenge, approach, results,
  stack, timeline and a client quote, and relates to its client.
- **Clients** at `/clients`, each with a logo, a short profile and the case studies done for them.
- **Services** at `/services`, each with deliverables, a typical timeline, the person who leads it and related work.
- A **studio** page, a **team** directory at `/team`, **insights** at `/insights` and **careers** at `/careers`
  (roles say how to get in touch; there is no application form).
- A **client portal** at `/portal` with project rooms at `/portal/projects/...` and deliverables and brand assets at
  `/portal/files/...`, for the `client_tidewell`, `client_corvane` and `studio` user groups.
- **Contact**, **accessibility** and **search** at `/search?q=...`.

## How the client portal works

- Each project and deliverable has a `client_group` field naming the user group that may see it.
- [hv_portal.liquid](theme/web-templates/hv_portal.liquid),
  [hv_detail_projects.liquid](theme/web-templates/hv_detail_projects.liquid) and
  [hv_detail_deliverables.liquid](theme/web-templates/hv_detail_deliverables.liquid) build a list of the visitor's
  groups from `CurrentUser.UserGroups` on the server. A client sees only items for their own group, the `studio` group
  (and admins) see every client, and signed-out visitors get a sign-in prompt. A client who opens another client's
  project sees a "belongs to another client" notice instead of the content, and portal pages use a generic title and
  description so nothing leaks into the page head.
- Case studies, projects and deliverables use relationship fields to clients, projects and team members, so pages link to
  each other without duplicated data. Listings and search read the same items with `get_content_items`.
- Widget templates read their settings from `widget.settings`.

## Rebuild it

```bash
# From a Raytha 2.x install with RAYTHA_URL and RAYTHA_API_KEY set:
bash build.sh
```

`build.sh` generates seed art if needed, then runs [`scripts/build-example.sh`](../scripts/build-example.sh), which
imports the schema, pushes the theme, seeds content, creates the `studio`, `client_tidewell` and `client_corvane` user
groups, the site pages and menus, then runs `raytha check`.

To see the portal, create a public user in the admin, add them to `client_tidewell`, `client_corvane` or `studio`,
and sign in at `/account/login`.

## Notes

- Halverline Studio is fictional. Its clients, people, projects and files are invented.
- The portal sign-in is a Raytha website account for project updates and files. Invoices and contracts are not on the site.
- There are no payment, registration or job application forms on this site.

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
