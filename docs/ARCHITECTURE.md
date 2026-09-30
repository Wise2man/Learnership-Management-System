# Architecture

One Django project (`config/`) with six apps. Django renders HTML on the server (templates + Bootstrap 5).

```
Browser -> Django: middleware -> urls.py -> permission helper -> function view -> (form / service) -> model -> database
                                                                            \-> template -> HTML back to the browser
```

## Apps and what they own
| App | Models | Notes |
|---|---|---|
| accounts | User, FacilitatorProfile, StudentProfile | `User.role` = ADMIN / FACILITATOR / STUDENT. The course right is `FacilitatorProfile.can_manage_courses` |
| courses | Course, Unit | Only PUBLISHED courses appear on the home page. A Unit has one facilitator |
| enrollments | Application, Enrollment | Approving an Application creates an Enrollment |
| assessments | Test, TestResult, Feedback | One result per student per test; one feedback per result |
| attendance | ClassSession, AttendanceRecord | One record per student per session |
| core | (none) | Home, dashboards, permission rules, shared utilities |

## Relationships
```
User 1-1 FacilitatorProfile / StudentProfile
User 1-N Course (created_by)          Course 1-N Unit          User 1-N Unit (facilitator)
User 1-N Application  N-1 Course      Application 1-1 Enrollment
Unit 1-N Test 1-N TestResult 1-1 Feedback
Unit 1-N ClassSession 1-N AttendanceRecord
```

## Access control

Enforce authorization on the server with shared permission functions/decorators in `core/permissions.py`; template link visibility is only a convenience. Scope reads so learners and facilitators see only records they are allowed to access. Add tests for role checks and object ownership.

New and updated endpoints use function-based views. The class-based views and mixins in the starter are legacy scaffold and should not be copied into new work; see `docs/APP_OWNERSHIP.md`.

## URL map
See `docs/TASK_MAP.md` and each app's `urls.py`. Fixed words (`courses/manage/`, `courses/create/`) must come
**before** `courses/<slug>/` in `courses/urls.py`.

## Settings
`config/settings/base.py` (shared), `dev.py` (default for manage.py), `prod.py` (used by wsgi/asgi). Values come from `.env`.
Default database is SQLite; set `DATABASE_URL` for PostgreSQL.
