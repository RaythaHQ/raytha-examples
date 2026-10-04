# Screenshots

A curated set, captured at 1440px (desktop) and 390px (phone) from a site built with `../build.sh`.
The images are hosted in the raytha.com media library. Click one for the full-size file.

| Screenshot | Shows |
|------------|-------|
| [![](https://raytha.com/raytha/media-items/objectkey/gk6fvObkGECGJo67ivubyg_lantern_ramblers_01_home_hero.webp)](https://raytha.com/raytha/media-items/objectkey/gk6fvObkGECGJo67ivubyg_lantern_ramblers_01_home_hero.webp) | Home, above the fold |
| [![](https://raytha.com/raytha/media-items/objectkey/Qw7DwB1q5kCSp_B4b6WTPQ_lantern_ramblers_02_home_full.webp)](https://raytha.com/raytha/media-items/objectkey/Qw7DwB1q5kCSp_B4b6WTPQ_lantern_ramblers_02_home_full.webp) | Home, full page |
| [![](https://raytha.com/raytha/media-items/objectkey/r82zCDkguUGgws6TOmT33g_lantern_ramblers_03_tour.webp)](https://raytha.com/raytha/media-items/objectkey/r82zCDkguUGgws6TOmT33g_lantern_ramblers_03_tour.webp) | Tour: upcoming and past shows |
| [![](https://raytha.com/raytha/media-items/objectkey/hgIAP-B-F0i3i2HBAGCT7w_lantern_ramblers_04_songs.webp)](https://raytha.com/raytha/media-items/objectkey/hgIAP-B-F0i3i2HBAGCT7w_lantern_ramblers_04_songs.webp) | Song stats |
| [![](https://raytha.com/raytha/media-items/objectkey/1WSd-LUryUihWZY-AmBIIA_lantern_ramblers_05_setlists.webp)](https://raytha.com/raytha/media-items/objectkey/1WSd-LUryUihWZY-AmBIIA_lantern_ramblers_05_setlists.webp) | The setlist archive |
| [![](https://raytha.com/raytha/media-items/objectkey/0Xe4GI-JnUawAEFJVGlTdA_lantern_ramblers_06_setlists_song.webp)](https://raytha.com/raytha/media-items/objectkey/0Xe4GI-JnUawAEFJVGlTdA_lantern_ramblers_06_setlists_song.webp) | The archive filtered to one song |
| [![](https://raytha.com/raytha/media-items/objectkey/SYpJA8XSLESAOPq-RKqpXg_lantern_ramblers_07_setlist_detail.webp)](https://raytha.com/raytha/media-items/objectkey/SYpJA8XSLESAOPq-RKqpXg_lantern_ramblers_07_setlist_detail.webp) | A single setlist |
| [![](https://raytha.com/raytha/media-items/objectkey/jcMG5K2FgEOjYmhMFJ3HEQ_lantern_ramblers_08_show_detail.webp)](https://raytha.com/raytha/media-items/objectkey/jcMG5K2FgEOjYmhMFJ3HEQ_lantern_ramblers_08_show_detail.webp) | An upcoming show |
| [![](https://raytha.com/raytha/media-items/objectkey/6J0A4T2ngEqXZikO_nYOnQ_lantern_ramblers_09_band.webp)](https://raytha.com/raytha/media-items/objectkey/6J0A4T2ngEqXZikO_nYOnQ_lantern_ramblers_09_band.webp) | The band |
| [![](https://raytha.com/raytha/media-items/objectkey/qUUq-KTAAk66dT3mmm037A_lantern_ramblers_10_member.webp)](https://raytha.com/raytha/media-items/objectkey/qUUq-KTAAk66dT3mmm037A_lantern_ramblers_10_member.webp) | A band member's page |
| [![](https://raytha.com/raytha/media-items/objectkey/BcXDxGPqHk24nQZr3mCqZQ_lantern_ramblers_11_media.webp)](https://raytha.com/raytha/media-items/objectkey/BcXDxGPqHk24nQZr3mCqZQ_lantern_ramblers_11_media.webp) | Photos, video and recordings |
| [![](https://raytha.com/raytha/media-items/objectkey/x7Ze11u6fEWkYP4eAMqNug_lantern_ramblers_12_booking.webp)](https://raytha.com/raytha/media-items/objectkey/x7Ze11u6fEWkYP4eAMqNug_lantern_ramblers_12_booking.webp) | Booking info and inquiry form |
| [<img src="https://raytha.com/raytha/media-items/objectkey/Aje9RP7fnkiWJ1yTFp7cDQ_lantern_ramblers_13_home_mobile.webp" width="200">](https://raytha.com/raytha/media-items/objectkey/Aje9RP7fnkiWJ1yTFp7cDQ_lantern_ramblers_13_home_mobile.webp) | Home on a phone |
| [<img src="https://raytha.com/raytha/media-items/objectkey/OKKvcN_pE0-9RK4yXliDxA_lantern_ramblers_14_tour_mobile.webp" width="200">](https://raytha.com/raytha/media-items/objectkey/OKKvcN_pE0-9RK4yXliDxA_lantern_ramblers_14_tour_mobile.webp) | Tour on a phone |
| [<img src="https://raytha.com/raytha/media-items/objectkey/9Jzk66vj5kK6yH4gACbD0Q_lantern_ramblers_15_songs_mobile.webp" width="200">](https://raytha.com/raytha/media-items/objectkey/9Jzk66vj5kK6yH4gACbD0Q_lantern_ramblers_15_songs_mobile.webp) | Song stats on a phone |
| [<img src="https://raytha.com/raytha/media-items/objectkey/VSIO8hEUbEytzQVUvXfL8A_lantern_ramblers_16_setlist_mobile.webp" width="200">](https://raytha.com/raytha/media-items/objectkey/VSIO8hEUbEytzQVUvXfL8A_lantern_ramblers_16_setlist_mobile.webp) | A setlist on a phone |

To capture your own (PNG, into this folder):

```bash
pip install playwright && playwright install chromium
BASE_URL=http://localhost:5001 python3 ../../scripts/capture-screenshots.py ../shots.json .
```
