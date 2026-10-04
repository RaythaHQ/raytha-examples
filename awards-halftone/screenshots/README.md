# Screenshots

A curated set, captured at 1440px (desktop) and 390px (phone) from a site built with `../build.sh`.
The images are hosted in the raytha.com media library. Click one for the full-size file.

| Screenshot | Shows |
|------------|-------|
| [![](https://raytha.com/raytha/media-items/objectkey/ysBc0hzkM0y7qJE-PF8QPQ_halftone_awards_01_home_hero.webp)](https://raytha.com/raytha/media-items/objectkey/ysBc0hzkM0y7qJE-PF8QPQ_halftone_awards_01_home_hero.webp) | Home, above the fold |
| [![](https://raytha.com/raytha/media-items/objectkey/mHUjWaChCEioibUxv4M_yQ_halftone_awards_02_home_full.webp)](https://raytha.com/raytha/media-items/objectkey/mHUjWaChCEioibUxv4M_yQ_halftone_awards_02_home_full.webp) | Home, full page |
| [![](https://raytha.com/raytha/media-items/objectkey/eVXIYQQcrkK1BLppkJpTHw_halftone_awards_03_categories.webp)](https://raytha.com/raytha/media-items/objectkey/eVXIYQQcrkK1BLppkJpTHw_halftone_awards_03_categories.webp) | Categories with deadlines |
| [![](https://raytha.com/raytha/media-items/objectkey/CBrqz7g700Cx8XmACVU0SQ_halftone_awards_04_category.webp)](https://raytha.com/raytha/media-items/objectkey/CBrqz7g700Cx8XmACVU0SQ_halftone_awards_04_category.webp) | A category page |
| [![](https://raytha.com/raytha/media-items/objectkey/pYzFtp4xm0KNDxFES6e33g_halftone_awards_05_gallery.webp)](https://raytha.com/raytha/media-items/objectkey/pYzFtp4xm0KNDxFES6e33g_halftone_awards_05_gallery.webp) | Entry gallery |
| [![](https://raytha.com/raytha/media-items/objectkey/37rdVtFZd0-RqHbV9iwDOQ_halftone_awards_06_entry.webp)](https://raytha.com/raytha/media-items/objectkey/37rdVtFZd0-RqHbV9iwDOQ_halftone_awards_06_entry.webp) | An entry page |
| [![](https://raytha.com/raytha/media-items/objectkey/b2C4wQIZ5E6Chee77UyIPw_halftone_awards_07_winners.webp)](https://raytha.com/raytha/media-items/objectkey/b2C4wQIZ5E6Chee77UyIPw_halftone_awards_07_winners.webp) | Past winners |
| [![](https://raytha.com/raytha/media-items/objectkey/5P3vyYAnoEWvNlTtCIwpFQ_halftone_awards_08_apply.webp)](https://raytha.com/raytha/media-items/objectkey/5P3vyYAnoEWvNlTtCIwpFQ_halftone_awards_08_apply.webp) | Entry form |
| [![](https://raytha.com/raytha/media-items/objectkey/Z58WQDo3i0C9pApmEuCfcg_halftone_awards_09_nominate.webp)](https://raytha.com/raytha/media-items/objectkey/Z58WQDo3i0C9pApmEuCfcg_halftone_awards_09_nominate.webp) | Nomination form |
| [![](https://raytha.com/raytha/media-items/objectkey/GifD5YtiS06jL3kCcOmrrQ_halftone_awards_10_thanks.webp)](https://raytha.com/raytha/media-items/objectkey/GifD5YtiS06jL3kCcOmrrQ_halftone_awards_10_thanks.webp) | Thank-you page |
| [![](https://raytha.com/raytha/media-items/objectkey/HjkwP2v4SEGvCIyqjRcGWQ_halftone_awards_11_jury.webp)](https://raytha.com/raytha/media-items/objectkey/HjkwP2v4SEGvCIyqjRcGWQ_halftone_awards_11_jury.webp) | The jury |
| [![](https://raytha.com/raytha/media-items/objectkey/WKFobFHrdEWHpAuOxwEB7A_halftone_awards_12_rules.webp)](https://raytha.com/raytha/media-items/objectkey/WKFobFHrdEWHpAuOxwEB7A_halftone_awards_12_rules.webp) | Rules |
| [<img src="https://raytha.com/raytha/media-items/objectkey/AxZf_G-i70uGkszdfiw7Dg_halftone_awards_13_home_mobile.webp" width="200">](https://raytha.com/raytha/media-items/objectkey/AxZf_G-i70uGkszdfiw7Dg_halftone_awards_13_home_mobile.webp) | Home on a phone |
| [<img src="https://raytha.com/raytha/media-items/objectkey/pcbcsLgUUEqx_EZeaLQY2w_halftone_awards_14_entry_mobile.webp" width="200">](https://raytha.com/raytha/media-items/objectkey/pcbcsLgUUEqx_EZeaLQY2w_halftone_awards_14_entry_mobile.webp) | An entry on a phone |
| [<img src="https://raytha.com/raytha/media-items/objectkey/Q38kPuyvYUeQc88gh61b1g_halftone_awards_15_apply_mobile.webp" width="200">](https://raytha.com/raytha/media-items/objectkey/Q38kPuyvYUeQc88gh61b1g_halftone_awards_15_apply_mobile.webp) | The entry form on a phone |

To capture your own (PNG, into this folder):

```bash
pip install playwright && playwright install chromium
BASE_URL=http://localhost:5001 python3 ../../scripts/capture-screenshots.py ../shots.json .
```
