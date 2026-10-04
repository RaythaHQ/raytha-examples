# Screenshots

A curated set, captured at 1440px (desktop) and 390px (phone) from a site built with `../build.sh`.
The images are hosted in the raytha.com media library. Click one for the full-size file.

| Screenshot | Shows |
|------------|-------|
| [![](https://raytha.com/raytha/media-items/objectkey/ghlpZ1oiZECxM06Pjao6AQ_lowtide_01_home_hero.webp)](https://raytha.com/raytha/media-items/objectkey/ghlpZ1oiZECxM06Pjao6AQ_lowtide_01_home_hero.webp) | Home, above the fold |
| [![](https://raytha.com/raytha/media-items/objectkey/ynnMJ6TXokuuWFLsbBiXGA_lowtide_02_home_full.webp)](https://raytha.com/raytha/media-items/objectkey/ynnMJ6TXokuuWFLsbBiXGA_lowtide_02_home_full.webp) | Home, full page |
| [![](https://raytha.com/raytha/media-items/objectkey/_qWc46kQQ0OYp5N8W1-Qgw_lowtide_03_lineup.webp)](https://raytha.com/raytha/media-items/objectkey/_qWc46kQQ0OYp5N8W1-Qgw_lowtide_03_lineup.webp) | Lineup with filters and stars |
| [![](https://raytha.com/raytha/media-items/objectkey/HDRl6wBGEEKiH_ZNkbkaXg_lowtide_04_lineup_filtered.webp)](https://raytha.com/raytha/media-items/objectkey/HDRl6wBGEEKiH_ZNkbkaXg_lowtide_04_lineup_filtered.webp) | Lineup filtered to Saturday and electronic |
| [![](https://raytha.com/raytha/media-items/objectkey/JyFIqn2kIUW23H5ryW-hAg_lowtide_05_schedule.webp)](https://raytha.com/raytha/media-items/objectkey/JyFIqn2kIUW23H5ryW-hAg_lowtide_05_schedule.webp) | Schedule grid, Friday, with starred sets |
| [![](https://raytha.com/raytha/media-items/objectkey/PDlAjd-JXkOZPkdWGio2-w_lowtide_06_artist.webp)](https://raytha.com/raytha/media-items/objectkey/PDlAjd-JXkOZPkdWGio2-w_lowtide_06_artist.webp) | An artist page |
| [![](https://raytha.com/raytha/media-items/objectkey/Tkd7Xp98dEGX52JT8DaaiQ_lowtide_07_venue.webp)](https://raytha.com/raytha/media-items/objectkey/Tkd7Xp98dEGX52JT8DaaiQ_lowtide_07_venue.webp) | Venue map, stages and places |
| [![](https://raytha.com/raytha/media-items/objectkey/Jc3fNRB-S0WFemgV6_aa-Q_lowtide_08_stage.webp)](https://raytha.com/raytha/media-items/objectkey/Jc3fNRB-S0WFemgV6_aa-Q_lowtide_08_stage.webp) | A stage page |
| [![](https://raytha.com/raytha/media-items/objectkey/yRz64Qchk0KnOPitwJHK_w_lowtide_09_faq.webp)](https://raytha.com/raytha/media-items/objectkey/yRz64Qchk0KnOPitwJHK_w_lowtide_09_faq.webp) | FAQ with search |
| [![](https://raytha.com/raytha/media-items/objectkey/8e06AHcdzE6SaV8vp3eXPw_lowtide_10_tickets.webp)](https://raytha.com/raytha/media-items/objectkey/8e06AHcdzE6SaV8vp3eXPw_lowtide_10_tickets.webp) | Ticket passes (external links) |
| [![](https://raytha.com/raytha/media-items/objectkey/MUp8FPH97k--bPuNKTyVJQ_lowtide_11_info.webp)](https://raytha.com/raytha/media-items/objectkey/MUp8FPH97k--bPuNKTyVJQ_lowtide_11_info.webp) | Plan your visit |
| [<img src="https://raytha.com/raytha/media-items/objectkey/eSeyvMDIOEW6J_me7Y7plw_lowtide_12_home_mobile.webp" width="200">](https://raytha.com/raytha/media-items/objectkey/eSeyvMDIOEW6J_me7Y7plw_lowtide_12_home_mobile.webp) | Home on a phone |
| [<img src="https://raytha.com/raytha/media-items/objectkey/Fpu-RRRl4UqxyBB4M0saDQ_lowtide_13_lineup_mobile.webp" width="200">](https://raytha.com/raytha/media-items/objectkey/Fpu-RRRl4UqxyBB4M0saDQ_lowtide_13_lineup_mobile.webp) | Lineup on a phone |
| [<img src="https://raytha.com/raytha/media-items/objectkey/g8X6eSG8YkWpSvzxCT1GRQ_lowtide_14_schedule_mobile.webp" width="200">](https://raytha.com/raytha/media-items/objectkey/g8X6eSG8YkWpSvzxCT1GRQ_lowtide_14_schedule_mobile.webp) | Schedule on a phone |
| [<img src="https://raytha.com/raytha/media-items/objectkey/Z3V8YQVwRUGLU9aUmJ-9wA_lowtide_15_artist_mobile.webp" width="200">](https://raytha.com/raytha/media-items/objectkey/Z3V8YQVwRUGLU9aUmJ-9wA_lowtide_15_artist_mobile.webp) | An artist on a phone |

To capture your own (PNG, into this folder):

```bash
pip install playwright && playwright install chromium
BASE_URL=http://localhost:5001 python3 ../../scripts/capture-screenshots.py ../shots.json .
```
