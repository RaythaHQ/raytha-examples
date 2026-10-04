# Screenshots

A curated set, captured at 1440px (desktop) and 390px (phone) from a site built with `../build.sh`.
The images are hosted in the raytha.com media library. Click one for the full-size file.

| Screenshot | Shows |
|------------|-------|
| [![](https://raytha.com/raytha/media-items/objectkey/6t-jZhocvEqtk0SbE02k_A_groundwork_01_home_hero.webp)](https://raytha.com/raytha/media-items/objectkey/6t-jZhocvEqtk0SbE02k_A_groundwork_01_home_hero.webp) | Home, above the fold |
| [![](https://raytha.com/raytha/media-items/objectkey/WlLc1jiupUaEVQrO4iEI8w_groundwork_02_home_full.webp)](https://raytha.com/raytha/media-items/objectkey/WlLc1jiupUaEVQrO4iEI8w_groundwork_02_home_full.webp) | Home, full page |
| [![](https://raytha.com/raytha/media-items/objectkey/jDTwRtvMTUqV17iR-_VbzA_groundwork_03_jobs.webp)](https://raytha.com/raytha/media-items/objectkey/jDTwRtvMTUqV17iR-_VbzA_groundwork_03_jobs.webp) | All jobs |
| [![](https://raytha.com/raytha/media-items/objectkey/p7xjsbIEx0yMYOC3D1bSxA_groundwork_04_jobs_filtered.webp)](https://raytha.com/raytha/media-items/objectkey/p7xjsbIEx0yMYOC3D1bSxA_groundwork_04_jobs_filtered.webp) | Software engineering, remote, top of band $130k+ |
| [![](https://raytha.com/raytha/media-items/objectkey/k5NRfj7WBkG2sHfJxFlU5w_groundwork_05_jobs_search.webp)](https://raytha.com/raytha/media-items/objectkey/k5NRfj7WBkG2sHfJxFlU5w_groundwork_05_jobs_search.webp) | Search for "battery", including company matches |
| [![](https://raytha.com/raytha/media-items/objectkey/z85eWxVh3UGWYriZdmQb4g_groundwork_06_job_detail.webp)](https://raytha.com/raytha/media-items/objectkey/z85eWxVh3UGWYriZdmQb4g_groundwork_06_job_detail.webp) | Job page with Apply link, facts and similar roles |
| [![](https://raytha.com/raytha/media-items/objectkey/4PhN07UE5USi5qwvSiSoUQ_groundwork_07_companies.webp)](https://raytha.com/raytha/media-items/objectkey/4PhN07UE5USi5qwvSiSoUQ_groundwork_07_companies.webp) | Company directory |
| [![](https://raytha.com/raytha/media-items/objectkey/kfO6DNyDdk-h4C6l7c55ug_groundwork_08_company_detail.webp)](https://raytha.com/raytha/media-items/objectkey/kfO6DNyDdk-h4C6l7c55ug_groundwork_08_company_detail.webp) | Company profile with its open roles |
| [![](https://raytha.com/raytha/media-items/objectkey/M3OlEhQqaESyDVykVPzJ6A_groundwork_09_remote.webp)](https://raytha.com/raytha/media-items/objectkey/M3OlEhQqaESyDVykVPzJ6A_groundwork_09_remote.webp) | Remote-only view filtered to Python |
| [![](https://raytha.com/raytha/media-items/objectkey/vrjOx0NZJkWvAqYpiTC7mg_groundwork_10_about.webp)](https://raytha.com/raytha/media-items/objectkey/vrjOx0NZJkWvAqYpiTC7mg_groundwork_10_about.webp) | About and FAQ |
| [![](https://raytha.com/raytha/media-items/objectkey/cHgxZi04hUOQagOrYQiPdA_groundwork_11_hub_locked.webp)](https://raytha.com/raytha/media-items/objectkey/cHgxZi04hUOQagOrYQiPdA_groundwork_11_hub_locked.webp) | Members' Hub, signed out |
| [![](https://raytha.com/raytha/media-items/objectkey/3OuQb2b_G0K1r7DeDXNJVQ_groundwork_12_hub_signed_in.webp)](https://raytha.com/raytha/media-items/objectkey/3OuQb2b_G0K1r7DeDXNJVQ_groundwork_12_hub_signed_in.webp) | Members' Hub, signed in as a member of `members` |
| [<img src="https://raytha.com/raytha/media-items/objectkey/EOcb9vEnqkKbppYthaGj3g_groundwork_13_home_mobile.webp" width="200">](https://raytha.com/raytha/media-items/objectkey/EOcb9vEnqkKbppYthaGj3g_groundwork_13_home_mobile.webp) | Home on a phone |
| [<img src="https://raytha.com/raytha/media-items/objectkey/Bhoc7BHPVUqSFQnTyM1VgA_groundwork_14_jobs_mobile.webp" width="200">](https://raytha.com/raytha/media-items/objectkey/Bhoc7BHPVUqSFQnTyM1VgA_groundwork_14_jobs_mobile.webp) | Job filters on a phone |
| [<img src="https://raytha.com/raytha/media-items/objectkey/uPhoqhTa_02wSPquKtEg0w_groundwork_15_job_mobile.webp" width="200">](https://raytha.com/raytha/media-items/objectkey/uPhoqhTa_02wSPquKtEg0w_groundwork_15_job_mobile.webp) | Job page on a phone |

To capture your own (PNG, into this folder):

```bash
pip install playwright && playwright install chromium
BASE_URL=http://localhost:5001 python3 ../../scripts/capture-screenshots.py ../shots.json .
```
