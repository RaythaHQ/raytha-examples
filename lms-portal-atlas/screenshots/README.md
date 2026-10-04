# Screenshots

A curated set, captured at 1440px (desktop) and 390px (phone) from a site built with `../build.sh`.
The images are hosted in the raytha.com media library. Click one for the full-size file.

| Screenshot | Shows |
|------------|-------|
| [![](https://raytha.com/raytha/media-items/objectkey/AJBqKggehkCGdW2HvJrzQA_atlas_lms_01_home_hero.webp)](https://raytha.com/raytha/media-items/objectkey/AJBqKggehkCGdW2HvJrzQA_atlas_lms_01_home_hero.webp) | Home, above the fold |
| [![](https://raytha.com/raytha/media-items/objectkey/CyYStlT3SEWyil9NNFS8wQ_atlas_lms_02_home_full.webp)](https://raytha.com/raytha/media-items/objectkey/CyYStlT3SEWyil9NNFS8wQ_atlas_lms_02_home_full.webp) | Home, full page |
| [![](https://raytha.com/raytha/media-items/objectkey/qf5tU19SDEqsmPZxjeHfJg_atlas_lms_03_catalog.webp)](https://raytha.com/raytha/media-items/objectkey/qf5tU19SDEqsmPZxjeHfJg_atlas_lms_03_catalog.webp) | Course catalog |
| [![](https://raytha.com/raytha/media-items/objectkey/vjdHUPRBnUuZvK3NK4cYLw_atlas_lms_04_course.webp)](https://raytha.com/raytha/media-items/objectkey/vjdHUPRBnUuZvK3NK4cYLw_atlas_lms_04_course.webp) | A course page |
| [![](https://raytha.com/raytha/media-items/objectkey/KlRRWKcPCEepvuOfbk7emQ_atlas_lms_05_free_lesson.webp)](https://raytha.com/raytha/media-items/objectkey/KlRRWKcPCEepvuOfbk7emQ_atlas_lms_05_free_lesson.webp) | A free preview lesson |
| [![](https://raytha.com/raytha/media-items/objectkey/uQct8UG0ikWy47-KwmJHuw_atlas_lms_06_locked_lesson.webp)](https://raytha.com/raytha/media-items/objectkey/uQct8UG0ikWy47-KwmJHuw_atlas_lms_06_locked_lesson.webp) | A members-only lesson, signed out |
| [![](https://raytha.com/raytha/media-items/objectkey/naIYBSbueEead8rk3VFOJg_atlas_lms_07_sign_in.webp)](https://raytha.com/raytha/media-items/objectkey/naIYBSbueEead8rk3VFOJg_atlas_lms_07_sign_in.webp) | Sign-in page |
| [![](https://raytha.com/raytha/media-items/objectkey/VUsqJI5AlU65AIKpwFPF7A_atlas_lms_08_member_lesson.webp)](https://raytha.com/raytha/media-items/objectkey/VUsqJI5AlU65AIKpwFPF7A_atlas_lms_08_member_lesson.webp) | The same lesson, signed in as a member |
| [![](https://raytha.com/raytha/media-items/objectkey/BNH7H8JNg0Wc7LYVLIApxA_atlas_lms_09_my_learning.webp)](https://raytha.com/raytha/media-items/objectkey/BNH7H8JNg0Wc7LYVLIApxA_atlas_lms_09_my_learning.webp) | My learning dashboard |
| [![](https://raytha.com/raytha/media-items/objectkey/5VZ5j42FWEaq0pjcbS0c9Q_atlas_lms_10_instructor.webp)](https://raytha.com/raytha/media-items/objectkey/5VZ5j42FWEaq0pjcbS0c9Q_atlas_lms_10_instructor.webp) | An instructor page |
| [![](https://raytha.com/raytha/media-items/objectkey/iZE0b08qRkSys0tf6XAMAg_atlas_lms_11_free_lessons.webp)](https://raytha.com/raytha/media-items/objectkey/iZE0b08qRkSys0tf6XAMAg_atlas_lms_11_free_lessons.webp) | All free lessons |
| [<img src="https://raytha.com/raytha/media-items/objectkey/iC4BOKxiHkqgkc87Xk1tbg_atlas_lms_12_home_mobile.webp" width="200">](https://raytha.com/raytha/media-items/objectkey/iC4BOKxiHkqgkc87Xk1tbg_atlas_lms_12_home_mobile.webp) | Home on a phone |
| [<img src="https://raytha.com/raytha/media-items/objectkey/8fnuHSiQmEic20S3DN5Sjg_atlas_lms_13_course_mobile.webp" width="200">](https://raytha.com/raytha/media-items/objectkey/8fnuHSiQmEic20S3DN5Sjg_atlas_lms_13_course_mobile.webp) | A course on a phone |
| [<img src="https://raytha.com/raytha/media-items/objectkey/8xayirnxE0edonp1sjFyrg_atlas_lms_14_locked_mobile.webp" width="200">](https://raytha.com/raytha/media-items/objectkey/8xayirnxE0edonp1sjFyrg_atlas_lms_14_locked_mobile.webp) | A locked lesson on a phone |

To capture your own (PNG, into this folder). The signed-in shots need a public user in the `students` group:

```bash
pip install playwright && playwright install chromium
export SITE_USER_EMAIL=you@example.com SITE_USER_PASSWORD='...'   # never commit these
BASE_URL=http://localhost:5001 python3 ../../scripts/capture-screenshots.py ../shots.json .
```
