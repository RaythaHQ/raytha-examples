# Brief: Horizon Summit 2027

The brief exactly as the agent got it. It is the only input it had.

> Build a website for a fictional annual tech conference, **Horizon Summit 2027**: three days in Austin, TX.
> Build it entirely on a Raytha instance with the `raytha` CLI. No clicking around the admin.

## Look and feel

- A striking custom theme that looks like a premium conference site, not a template: a bold full-bleed hero with an
  animated gradient or mesh background, large expressive type (a Google Fonts pairing), a rich dark palette, subtle
  CSS animation and hover effects, glass or card depth.
- Polished speaker photo grids, an elegant agenda timeline, a logo-wall sponsor section.
- Responsive. It has to look good on a phone as well as a desktop.
- Free or placeholder images only (generated SVGs or freely licensed images uploaded to the media library).

## Content model, with realistic seed content

- **Speakers** (about 12): bio, job title, company, photo.
- **Sessions** (about 20): linked to a speaker and a track, with day, start and end time, room and format.
- **Tracks**.
- **Sponsors** in platinum, gold and silver tiers.
- **News** and announcements.

## Pages

- Home: hero, key dates or a countdown, featured speakers, a sponsor wall.
- Agenda, filterable by day and by track (list views and query parameters).
- Speaker directory, plus a page per speaker that lists their sessions.
- A page per session.
- Sponsors, Venue and travel, FAQ.

## Functionality

- A members-only **Attendee Hub** page, gated by a Raytha user group.
- Site search.
- Navigation menus.
- Optionally a Raytha Function for something useful, such as an `.ics` calendar download per session or a JSON
  feed of the agenda.

## Done means

- `raytha check` passes with no broken routes.
- Screenshots of the result on desktop and mobile.
- The schema and theme exported so the site can be rebuilt or deployed elsewhere.
