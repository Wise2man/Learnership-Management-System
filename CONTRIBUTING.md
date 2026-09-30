# Contributing

## The 5 golden rules
1. Never work directly on `main` or `develop`. One branch per task: `feature/LMS-203-course-crud`.
2. Every change goes through a **Pull Request**. The lead reviews it.
3. Stuck for **30 minutes**? Ask in Slack (`#lms-blockers`).
4. Every page with a permission needs a **test**. A hidden button is not security.
5. Post your daily standup, even when there is nothing to report.

## Doing a task
1. Claim one primary app in the team task board (see `docs/APP_OWNERSHIP.md`), then choose an unblocked task in that app.
2. Post "Starting LMS-xxx" in the task thread; set status **In progress**.
3. `git checkout develop && git pull && git checkout -b feature/LMS-xxx-short-name`
4. Build in small steps. Run the site often.
5. Write tests. Run `make check`.
6. Commit: `LMS-xxx: what you did` (task number first).
7. Push, open a Pull Request (the template asks the right questions). Set status **In review**.
8. Fix every review comment. After merge: delete the branch, set **Done**, write your real hours.

## Code rules
* New and updated endpoints must be function-based views. Do not add class-based views or mixins; use shared server-side permission functions/decorators.
* Business rules in `services.py`; reusable queries in `selectors.py`; keep views short.
* Use URL names (`{% url 'courses:detail' slug=course.slug %}`), never typed paths.
* Use `settings.AUTH_USER_MODEL` in foreign keys.
* Use `select_related` / `prefetch_related` on list pages.
* Wrap multi-step saves (approve + enroll, marks, attendance) in `transaction.atomic()`.
* Never edit a migration that is already merged. Make a new one.
* Never commit `.env`, passwords or keys.
* Ask the model's owner before changing their models (see `docs/TASK_MAP.md`).

## Review labels
**Must fix** (blocks merge) / **Should fix** (please do) / **Idea** (optional).
