# Commonground Association: a membership association with a members-only library

The website for Commonground, a fictional nonprofit association for community gardeners with eight local chapters,
built on Raytha 2.0.1 by an AI agent with the [`raytha` CLI](https://github.com/RaythaHQ/raytha-cli). Every
template, content type, item, page, user group and menu went in through the CLI. Nobody opened the admin.

- **Brief:** [brief.md](brief.md)
- **Build time:** about an hour of agent time, from an empty install to `raytha check` passing
- **Write-up:** [raytha.com/use-cases/commonground-association](https://raytha.com/use-cases/commonground-association)
- **Walkthrough video:** [MP4, 39 s](https://raytha.com/raytha/media-items/objectkey/tHS4mIpgl0GpjpkBIXUCbA_commonground_association_walkthrough.mp4) (shot list: [walkthrough.json](walkthrough.json))

![Commonground home page](https://raytha.com/raytha/media-items/objectkey/UuInALAw5UuRF91xAq6tOg_commonground_01_home_hero.webp)

## Screenshots

| | |
|---|---|
| ![Membership tiers](https://raytha.com/raytha/media-items/objectkey/1LcfWh4lDk6_vJ1YCgq2_A_commonground_03_membership.webp) | ![Chapter directory](https://raytha.com/raytha/media-items/objectkey/JXjcz-1K0EO0Xdd1d8h-HQ_commonground_05_chapters.webp) |
| Four tiers; Join buttons go to an external partner, no payments on the site | The chapter map and directory with region filters |
| ![A locked resource](https://raytha.com/raytha/media-items/objectkey/H-E9LNryxEuUzuHS9irqxA_commonground_10_resource_locked.webp) | ![Member dashboard](https://raytha.com/raytha/media-items/objectkey/yNSwy_HWakSAlWt0HIzhRQ_commonground_11_member_dashboard.webp) |
| A library resource as a visitor sees it | A member's dashboard after signing in |

<p>
  <img src="https://raytha.com/raytha/media-items/objectkey/wbxs2Rt4H0i1_8A3ReV1eA_commonground_15_home_mobile.webp" width="240" alt="Home on a phone">
  <img src="https://raytha.com/raytha/media-items/objectkey/gYkQ3eJD_EKSj3wjrwLz6w_commonground_16_chapters_mobile.webp" width="240" alt="Chapters on a phone">
  <img src="https://raytha.com/raytha/media-items/objectkey/JdTwCIRUd0SVnKA0rmzGdA_commonground_17_membership_mobile.webp" width="240" alt="Tiers on a phone">
</p>

More in [screenshots/](screenshots/). Recapture them from your own build with [shots.json](shots.json) and
[`scripts/capture-screenshots.py`](../scripts/capture-screenshots.py).

## What's in it

- A home page with member benefits, the next four events, the tiers, the largest chapters, news and a call to join.
- A membership page at `/membership` with the tiers, three ways to join and an FAQ; a page per tier at
  `/membership/...` and a comparison at `/tiers`.
- A chapter directory at `/chapters` with an SVG pin map, region filters and chapter cards; each chapter page
  lists its lead, meeting time and upcoming events.
- Events at `/events`, filterable by format (`?format=in_person|online|hybrid`) and audience
  (`?audience=members`). Past events move to a "Recently" list by themselves.
- News at `/news` with topic filters and a lead story.
- A resource library at `/resources`: the list is public, the full resource is members-only.
- A members dashboard at `/members` and a restyled sign-in page.

## Joining and payments

The site takes no payments. Join buttons link to `https://join.example.org/commonground?tier=...`, a placeholder
for an external membership platform, and carry an external-link icon and a note saying so. The membership page
also offers a contact path and suggests coming to an open event first. Replace `join_url` in
[pages/home.json](pages/home.json) and [pages/membership.json](pages/membership.json), and the link in
[cg_detail_tiers.liquid](theme/web-templates/cg_detail_tiers.liquid), with your real join form.

## How the members area works

- `build.sh` creates a **user group** with the developer name `members` (from `groups` in [example.json](example.json)).
- Templates set `is_member` when `CurrentUser.UserGroups` contains `members` or the user is an admin.
  [cg_detail_resources.liquid](theme/web-templates/cg_detail_resources.liquid) renders the resource body only for
  members; everyone else gets a sign-in and join panel. The check runs on the server, so the members-only text is
  never sent to visitors.
- [cg_members.liquid](theme/web-templates/cg_members.liquid) is the dashboard. Signed-out visitors and signed-in
  users who are not in the group get a short explanation instead.

To see it unlocked, add a site user to the group:

```bash
GROUP=$(raytha user-group list --all | jq -r '(.data.items // .data)[] | select(.developerName=="members") | .id')
USER=$(raytha user create --email member@example.com --first-name Maya --last-name Ortiz --groups "$GROUP" | jq -r .data.id)
printf '%s' 'choose-a-password' | raytha user password "$USER" --password-stdin
```

## The Raytha features behind it

| Feature | How it's built |
|---------|----------------|
| Tiers, chapters, events, news, resources | Five **content types** in [schema.json](schema.json). Events have a **relationship field** to their chapter, a **date** for the start and **dropdowns** for format and audience. Tiers have a **checkbox** for the highlighted tier. |
| Seed content | `raytha content import` from JSON Lines in [seed/](seed/). Events point at their chapter by name; `@file:` values upload the SVG illustrations. |
| Directory, events, news, library | **List views** with **Liquid** templates. Query parameters are checked against the allowed values before they are used. |
| Chapter map | Each chapter's state maps to a pin position on an inline SVG; member and garden totals are summed in the template. |
| Members-only content | A **user group** and `CurrentUser.UserGroups` checks in the templates. |
| Sign in | Raytha's built-in **login**, with `raytha_html_base_login_layout` and `raytha_html_login_emailandpassword` restyled. |
| Home, Membership, About, Contact, My membership | **Site pages** built from 12 custom **widget templates**. |
| Navigation | Two **menus**, `mainmenu` and `footer`, in [menus/](menus/). The footer also lists the chapters from the content. |

## Rebuild it

You need a Raytha 2.x site you can wipe (a fresh install is best), an admin API key, the `raytha` CLI, `jq` and
`python3` (to draw the illustrations).
Follow steps 1 to 3 of the [Quickstart](../README.md#quickstart) to run Raytha, create a key and install the CLI, then:

```bash
cd association-commonground
DRY_RUN=1 bash build.sh     # previews the schema import, changes nothing
bash build.sh
```

`build.sh` first draws the 15 garden SVGs into `seed/art/` with [seed/make-art.py](seed/make-art.py) if they are
not there yet. It then runs the shared [scripts/build-example.sh](../scripts/build-example.sh) with this folder's
[example.json](example.json): it pushes and activates the `commonground` theme, imports the schema, binds every
view to its list template, imports the 35 seed items, creates the `members` group, the five site pages and both
menus, then runs `raytha check`. You can run it again: everything is created or updated in place, and seed content
only goes into content types that are still empty.

## Files

| Path | What it is |
|------|------------|
| [brief.md](brief.md) | The brief the agent got |
| [build.sh](build.sh) | Rebuild script (`RAYTHA_URL`, `RAYTHA_API_KEY` from env) |
| [example.json](example.json) | Theme name, import order, detail templates and the members group |
| [schema.json](schema.json) | Content types, fields, choices and views (`raytha schema import`) |
| [theme/](theme/) | The `commonground` theme: `cg_*` web and widget templates, the base layout, login templates and 404 page |
| [seed/](seed/) | Tiers, chapters, events, news and resources as JSON Lines, plus [make-art.py](seed/make-art.py) |
| [pages/](pages/) | Site page sections and `pages.json` (title, route, template) |
| [menus/](menus/) | Main and footer menu items |
| [shots.json](shots.json) | The screenshot list for `scripts/capture-screenshots.py` |
| [walkthrough.json](walkthrough.json) | The shot list for [`scripts/make-walkthrough.py`](../scripts/make-walkthrough.md) |

## Notes

- Commonground, its chapters, people and events are fictional. Email addresses use `example.org` and
  `commonground.example`. The illustrations are generated SVG, so every image is license-free.
- Fonts: Fraunces for headlines and Public Sans for text, from Google Fonts. Bootstrap Icons load from jsDelivr.
- The "Download" button on an unlocked resource is a placeholder. In a real site, attach the file to the resource
  with an attachment field and link it for members only.
- Raytha's Liquid does not allow parentheses in conditions. Combine filters with flags, as
  [cg_list_events.liquid](theme/web-templates/cg_list_events.liquid) does.
- Dropdown and checkbox values are objects in Liquid; capture them into a string first
  (`{% capture fm %}{{ p.format }}{% endcapture %}`). Checkboxes render `True`.
