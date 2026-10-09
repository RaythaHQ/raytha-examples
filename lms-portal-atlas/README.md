# Atlas Learning: a course portal with members-only lessons

The public portal for Atlas Learning, a fictional online school, built on Raytha 2.0.1 by an AI agent with the
[`raytha` CLI](https://github.com/RaythaHQ/raytha-cli). Every template, content type, course, lesson, page, menu
and user group went in through the CLI. Nobody opened the admin.

- **Brief:** [brief.md](brief.md)
- **Build time:** about 40 minutes of agent time, from an empty install to `raytha check` passing
- **Write-up:** [raytha.com/use-cases/atlas-learning-portal](https://raytha.com/use-cases/atlas-learning-portal)
- **Walkthrough video:** [MP4, 34 s](https://raytha.com/raytha/media-items/objectkey/lWLEOS8HTkGjXHxXdgeczw_atlas_learning_portal_walkthrough.mp4) (shot list: [walkthrough.json](walkthrough.json))

![Atlas Learning home page](https://raytha.com/raytha/media-items/objectkey/AJBqKggehkCGdW2HvJrzQA_atlas_lms_01_home_hero.webp)

## Screenshots

| | |
|---|---|
| ![Course page](https://raytha.com/raytha/media-items/objectkey/vjdHUPRBnUuZvK3NK4cYLw_atlas_lms_04_course.webp) | ![Locked lesson](https://raytha.com/raytha/media-items/objectkey/uQct8UG0ikWy47-KwmJHuw_atlas_lms_06_locked_lesson.webp) |
| Course page with modules and locked lessons | A members-only lesson, as a visitor sees it |
| ![Member lesson](https://raytha.com/raytha/media-items/objectkey/VUsqJI5AlU65AIKpwFPF7A_atlas_lms_08_member_lesson.webp) | ![My learning](https://raytha.com/raytha/media-items/objectkey/BNH7H8JNg0Wc7LYVLIApxA_atlas_lms_09_my_learning.webp) |
| The same lesson for a signed-in member | My learning, with progress per course |

<p>
  <img src="https://raytha.com/raytha/media-items/objectkey/iC4BOKxiHkqgkc87Xk1tbg_atlas_lms_12_home_mobile.webp" width="240" alt="Home on a phone">
  <img src="https://raytha.com/raytha/media-items/objectkey/8xayirnxE0edonp1sjFyrg_atlas_lms_14_locked_mobile.webp" width="240" alt="Locked lesson on a phone">
</p>

More in [screenshots/](screenshots/). Recapture them from your own build with [shots.json](shots.json) and
[`scripts/capture-screenshots.py`](../scripts/capture-screenshots.py).

## What's in it

- A home page with a stack of course covers, topic tiles with live course counts, popular courses, a "how it
  works" strip, the instructors and a membership band.
- A course catalog at `/courses`, filterable by topic and level, with a search box.
- Course pages with outcomes, a description and the curriculum grouped into modules, with a lock on every lesson
  that needs a membership.
- Lesson pages with the course outline, a video-style player or reading header, the lesson, and previous and next
  links.
- Free preview lessons that anyone can open, collected at `/free-lessons`.
- Members-only lessons: for visitors who are not members, the template renders a locked panel instead of the
  lesson, so the lesson text never leaves the server.
- A members-only "My learning" dashboard at `/my-learning` with progress bars and a resume button. Members mark
  lessons complete as they go; progress is kept in the browser (`localStorage`).
- A restyled sign-in page and 404 page, and instructor pages with their courses.

## The Raytha features behind it

| Feature | How it's built |
|---------|----------------|
| Instructors, courses, lessons | Three **content types** in [schema.json](schema.json). Courses have a **relationship field** to their instructor, **dropdowns** for topic and level, **numbers**, an **attachment** cover, a **colour** and a **checkbox** for featured. Lessons point at their course and carry a module name and number, a lesson number, a length, a format and a free preview checkbox. |
| Seed content | `raytha content import` from JSON Lines in [seed/](seed/). Lessons point at their course by title; `@file:` values upload the SVG covers and portraits. |
| Members-only lessons | The `students` **user group** (created by the build from [example.json](example.json)). Templates loop over `CurrentUser.UserGroups` and only render lesson bodies for members or free previews. |
| Sign-in | Raytha's built-in public user login, restyled in `raytha_html_base_login_layout` and `raytha_html_login_emailandpassword`. |
| Course catalog | A **list view** at `/courses`. The **Liquid** template reads `?category=`, `?level=` and `?q=`, checks each against a known list and builds a filter for `get_content_items`. |
| Curriculum | The course template queries `course eq '<id>'`, orders by lesson number, groups by module and adds up the minutes. |
| Home, membership and My learning | **Site pages**. Home and membership are built from 8 custom **widget templates**; My learning uses its own members-only template. |
| Navigation | Two **menus**, `mainmenu` and `footer`, in [menus/](menus/). |

## Rebuild it

[![Deploy on Railway](https://railway.com/button.svg)](https://raytha.com/go/railway?from=examples-lms-portal-atlas)

Deploy Raytha first, then import this kit. The button deploys a fresh Raytha with PostgreSQL on Railway; finish the setup wizard, create an API key, and run `build.sh` below against the new site.

You need a Raytha 2.x site you can wipe (a fresh install is best), an admin API key, the `raytha` CLI, and `jq`.
Follow steps 1 to 3 of the [Quickstart](../README.md#quickstart) to run Raytha, create a key and install the CLI, then:

```bash
cd lms-portal-atlas
DRY_RUN=1 bash build.sh     # previews the schema import, changes nothing
bash build.sh
```

`build.sh` runs the shared [scripts/build-example.sh](../scripts/build-example.sh) with this folder's
[example.json](example.json). It pushes and activates the `atlas` theme, imports the schema, binds every view to
its list template, imports the seed content with its artwork, creates the `students` user group, the three site
pages and both menus, then runs `raytha check`. You can run it again: everything is created or updated in place,
and seed content only goes into content types that are still empty.

To see the members' side, create a public user in the `students` group (in the admin under Users, or with the CLI)
and sign in at `/account/login`:

```bash
raytha user-group list                       # note the id of "students"
raytha user create --email you@example.com --first-name Your --last-name Name --groups <students-group-id>
raytha user password <user-id> --password-stdin
```

Use a public site user for this, never an admin account.

## Files

| Path | What it is |
|------|------------|
| [brief.md](brief.md) | The brief the agent got |
| [build.sh](build.sh) | Rebuild script (`RAYTHA_URL`, `RAYTHA_API_KEY` from env) |
| [example.json](example.json) | Theme name, import order, detail templates and the `students` group for the shared build script |
| [schema.json](schema.json) | Content types, fields, choices and views (`raytha schema import`) |
| [theme/](theme/) | The `atlas` theme: the `al_*` web and widget templates plus the restyled base layout, login and 404 pages |
| [seed/](seed/) | Instructors, courses and lessons as JSON Lines, plus the SVG covers and portraits and [make-art.py](seed/make-art.py) that draws them |
| [pages/](pages/) | Site page sections and `pages.json` (title, route, template) |
| [menus/](menus/) | Main and footer menu items |
| [shots.json](shots.json) | The screenshot list for `scripts/capture-screenshots.py` (signed-in shots need `SITE_USER_EMAIL` and `SITE_USER_PASSWORD`) |
| [walkthrough.json](walkthrough.json) | The shot list for [`scripts/make-walkthrough.py`](../scripts/make-walkthrough.md) |

## Notes

- Atlas Learning, its instructors and its courses are fictional. Portraits and covers are drawn from simple SVG
  shapes. Email links use `example.com`.
- Fonts: Bricolage Grotesque for headings, Figtree for text and JetBrains Mono for labels, from Google Fonts.
  Bootstrap Icons load from jsDelivr.
- There are no payments. The membership page explains how to get access by email.
- Lesson progress lives in each member's browser, so it does not follow them to another device. Saving it on the
  server would need a Function and a progress content type.
- Raytha's Liquid does not support `{% include %}` of other web templates, so the course card markup is repeated
  in the three templates that list courses.
