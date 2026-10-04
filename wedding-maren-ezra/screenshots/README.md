# Screenshots

A curated set, captured at 1440px (desktop) and 390px (phone) from a site built with `../build.sh`.
The images are hosted in the raytha.com media library. Click one for the full-size file.

| Screenshot | Shows |
|------------|-------|
| [![](https://raytha.com/raytha/media-items/objectkey/C0SAAyOVg0WlEbppl3brpQ_maren_ezra_wedding_01_home_hero.webp)](https://raytha.com/raytha/media-items/objectkey/C0SAAyOVg0WlEbppl3brpQ_maren_ezra_wedding_01_home_hero.webp) | Home, above the fold |
| [![](https://raytha.com/raytha/media-items/objectkey/MviqGQq3Qk-4tp-TDEsa3g_maren_ezra_wedding_02_home_full.webp)](https://raytha.com/raytha/media-items/objectkey/MviqGQq3Qk-4tp-TDEsa3g_maren_ezra_wedding_02_home_full.webp) | Home, full page |
| [![](https://raytha.com/raytha/media-items/objectkey/gHjL6X8Dt0KDTG5MJeNyew_maren_ezra_wedding_03_schedule.webp)](https://raytha.com/raytha/media-items/objectkey/gHjL6X8Dt0KDTG5MJeNyew_maren_ezra_wedding_03_schedule.webp) | The weekend schedule |
| [![](https://raytha.com/raytha/media-items/objectkey/4nxFzBscdUWUBSrdzBe4Zg_maren_ezra_wedding_04_story.webp)](https://raytha.com/raytha/media-items/objectkey/4nxFzBscdUWUBSrdzBe4Zg_maren_ezra_wedding_04_story.webp) | Our story |
| [![](https://raytha.com/raytha/media-items/objectkey/LF76BTW7HUyTnLKlxhxV3w_maren_ezra_wedding_05_travel.webp)](https://raytha.com/raytha/media-items/objectkey/LF76BTW7HUyTnLKlxhxV3w_maren_ezra_wedding_05_travel.webp) | Travel and hotel room blocks |
| [![](https://raytha.com/raytha/media-items/objectkey/YdOWaRHk6EKIpMI_yH8O_g_maren_ezra_wedding_06_things_to_do.webp)](https://raytha.com/raytha/media-items/objectkey/YdOWaRHk6EKIpMI_yH8O_g_maren_ezra_wedding_06_things_to_do.webp) | Things to do |
| [![](https://raytha.com/raytha/media-items/objectkey/-4o4vG2t9UOZh1sThEK79w_maren_ezra_wedding_07_faq.webp)](https://raytha.com/raytha/media-items/objectkey/-4o4vG2t9UOZh1sThEK79w_maren_ezra_wedding_07_faq.webp) | FAQ |
| [![](https://raytha.com/raytha/media-items/objectkey/W7UIIsPF5Em90zjq8PXnEw_maren_ezra_wedding_08_registry.webp)](https://raytha.com/raytha/media-items/objectkey/W7UIIsPF5Em90zjq8PXnEw_maren_ezra_wedding_08_registry.webp) | Registry |
| [![](https://raytha.com/raytha/media-items/objectkey/SMYLyx06lEuVYLgNSxImhw_maren_ezra_wedding_09_gallery.webp)](https://raytha.com/raytha/media-items/objectkey/SMYLyx06lEuVYLgNSxImhw_maren_ezra_wedding_09_gallery.webp) | Gallery |
| [![](https://raytha.com/raytha/media-items/objectkey/AS0bd9j3FUmc8qzMGkghsA_maren_ezra_wedding_10_rsvp.webp)](https://raytha.com/raytha/media-items/objectkey/AS0bd9j3FUmc8qzMGkghsA_maren_ezra_wedding_10_rsvp.webp) | RSVP form |
| [![](https://raytha.com/raytha/media-items/objectkey/kCD5NquwGk2ZMH4eAz_PDg_maren_ezra_wedding_11_thanks.webp)](https://raytha.com/raytha/media-items/objectkey/kCD5NquwGk2ZMH4eAz_PDg_maren_ezra_wedding_11_thanks.webp) | RSVP thank-you page |
| [![](https://raytha.com/raytha/media-items/objectkey/O3etDbJlHUitVvgKYSTbEA_maren_ezra_wedding_12_guests.webp)](https://raytha.com/raytha/media-items/objectkey/O3etDbJlHUitVvgKYSTbEA_maren_ezra_wedding_12_guests.webp) | Guest page (signed in) |
| [![](https://raytha.com/raytha/media-items/objectkey/99HGKcxEcEOgDrZgdCVawg_maren_ezra_wedding_13_event.webp)](https://raytha.com/raytha/media-items/objectkey/99HGKcxEcEOgDrZgdCVawg_maren_ezra_wedding_13_event.webp) | An event page |
| [<img src="https://raytha.com/raytha/media-items/objectkey/kHcD4Cn330KhLJ9yG5uzIw_maren_ezra_wedding_14_home_mobile.webp" width="200">](https://raytha.com/raytha/media-items/objectkey/kHcD4Cn330KhLJ9yG5uzIw_maren_ezra_wedding_14_home_mobile.webp) | Home on a phone |
| [<img src="https://raytha.com/raytha/media-items/objectkey/omz8quq08E622Uj7LrVIxg_maren_ezra_wedding_15_schedule_mobile.webp" width="200">](https://raytha.com/raytha/media-items/objectkey/omz8quq08E622Uj7LrVIxg_maren_ezra_wedding_15_schedule_mobile.webp) | The schedule on a phone |
| [<img src="https://raytha.com/raytha/media-items/objectkey/SWZTY1seK02ilINz4FvX2w_maren_ezra_wedding_16_rsvp_mobile.webp" width="200">](https://raytha.com/raytha/media-items/objectkey/SWZTY1seK02ilINz4FvX2w_maren_ezra_wedding_16_rsvp_mobile.webp) | The RSVP form on a phone |

To capture your own (PNG, into this folder):

```bash
pip install playwright && playwright install chromium
BASE_URL=http://localhost:5001 python3 ../../scripts/capture-screenshots.py ../shots.json .
```
