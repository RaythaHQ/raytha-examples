# Screenshots

A curated set, captured at 1440px (desktop) and 390px (phone) from a site built with `../build.sh`.
The images are hosted in the raytha.com media library. Click one for the full-size file.

| Screenshot | Shows |
|------------|-------|
| [![](https://raytha.com/raytha/media-items/objectkey/sJNessfzGUO96Rpjk_RQ2w_postmark_trips_01_home_hero.webp)](https://raytha.com/raytha/media-items/objectkey/sJNessfzGUO96Rpjk_RQ2w_postmark_trips_01_home_hero.webp) | Home, above the fold |
| [![](https://raytha.com/raytha/media-items/objectkey/Y64NlHLHEkSuXPwOGgyx8w_postmark_trips_02_home_full.webp)](https://raytha.com/raytha/media-items/objectkey/Y64NlHLHEkSuXPwOGgyx8w_postmark_trips_02_home_full.webp) | Home, full page |
| [![](https://raytha.com/raytha/media-items/objectkey/28t5_E0ebEOfY3flybZTRg_postmark_trips_03_how_it_works.webp)](https://raytha.com/raytha/media-items/objectkey/28t5_E0ebEOfY3flybZTRg_postmark_trips_03_how_it_works.webp) | How it works |
| [![](https://raytha.com/raytha/media-items/objectkey/rKfTBQMe8kuIFF6DVOFYUQ_postmark_trips_04_trips.webp)](https://raytha.com/raytha/media-items/objectkey/rKfTBQMe8kuIFF6DVOFYUQ_postmark_trips_04_trips.webp) | Trips and prices |
| [![](https://raytha.com/raytha/media-items/objectkey/IEjZf6Vl3UyY_oHXAc63rQ_postmark_trips_05_tier.webp)](https://raytha.com/raytha/media-items/objectkey/IEjZf6Vl3UyY_oHXAc63rQ_postmark_trips_05_tier.webp) | A tier page |
| [![](https://raytha.com/raytha/media-items/objectkey/bA7WWT_TtUKX9v4RFn5xSg_postmark_trips_06_reveals.webp)](https://raytha.com/raytha/media-items/objectkey/bA7WWT_TtUKX9v4RFn5xSg_postmark_trips_06_reveals.webp) | Past reveals as postcards |
| [![](https://raytha.com/raytha/media-items/objectkey/Q5BafdStHUeXIPLecnEofw_postmark_trips_07_reveal_detail.webp)](https://raytha.com/raytha/media-items/objectkey/Q5BafdStHUeXIPLecnEofw_postmark_trips_07_reveal_detail.webp) | A destination story |
| [![](https://raytha.com/raytha/media-items/objectkey/BnyhRnfnJ0yupSZnKLoMMw_postmark_trips_08_reviews.webp)](https://raytha.com/raytha/media-items/objectkey/BnyhRnfnJ0yupSZnKLoMMw_postmark_trips_08_reviews.webp) | Reviews with the rating breakdown |
| [![](https://raytha.com/raytha/media-items/objectkey/RV4Lwh7UnEmTqXZ4z8gfYQ_postmark_trips_09_faq.webp)](https://raytha.com/raytha/media-items/objectkey/RV4Lwh7UnEmTqXZ4z8gfYQ_postmark_trips_09_faq.webp) | FAQ by topic |
| [![](https://raytha.com/raytha/media-items/objectkey/_IhnP5boSkWiAFCRwIZgzA_postmark_trips_10_gift.webp)](https://raytha.com/raytha/media-items/objectkey/_IhnP5boSkWiAFCRwIZgzA_postmark_trips_10_gift.webp) | Gift a trip |
| [![](https://raytha.com/raytha/media-items/objectkey/i6BmltBfiES10xjI5uEsSA_postmark_trips_11_plan.webp)](https://raytha.com/raytha/media-items/objectkey/i6BmltBfiES10xjI5uEsSA_postmark_trips_11_plan.webp) | The trip planner |
| [![](https://raytha.com/raytha/media-items/objectkey/nQKLm7ZQZUWGQIq3jKANMA_postmark_trips_12_thanks.webp)](https://raytha.com/raytha/media-items/objectkey/nQKLm7ZQZUWGQIq3jKANMA_postmark_trips_12_thanks.webp) | Thank-you page after a request |
| [<img src="https://raytha.com/raytha/media-items/objectkey/FYIYJKyy_UWj_Q1Gfsn_iw_postmark_trips_13_home_mobile.webp" width="200">](https://raytha.com/raytha/media-items/objectkey/FYIYJKyy_UWj_Q1Gfsn_iw_postmark_trips_13_home_mobile.webp) | Home on a phone |
| [<img src="https://raytha.com/raytha/media-items/objectkey/DPaaXgQ_2EyS-6g-mBHPyA_postmark_trips_14_trips_mobile.webp" width="200">](https://raytha.com/raytha/media-items/objectkey/DPaaXgQ_2EyS-6g-mBHPyA_postmark_trips_14_trips_mobile.webp) | Trips on a phone |
| [<img src="https://raytha.com/raytha/media-items/objectkey/UHSagRzMQUuPpnW7szCv_g_postmark_trips_15_reveals_mobile.webp" width="200">](https://raytha.com/raytha/media-items/objectkey/UHSagRzMQUuPpnW7szCv_g_postmark_trips_15_reveals_mobile.webp) | Reveals on a phone |
| [<img src="https://raytha.com/raytha/media-items/objectkey/ObmiSMhlRkmrSYcc0X6J_Q_postmark_trips_16_plan_mobile.webp" width="200">](https://raytha.com/raytha/media-items/objectkey/ObmiSMhlRkmrSYcc0X6J_Q_postmark_trips_16_plan_mobile.webp) | The planner on a phone |

To capture your own (PNG, into this folder):

```bash
pip install playwright && playwright install chromium
BASE_URL=http://localhost:5001 python3 ../../scripts/capture-screenshots.py ../shots.json .
```
