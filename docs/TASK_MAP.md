# Task map: where to work for each task

Legend: **DONE** = already in the starter (read it, ask questions, improve it through a Pull Request), **STARTER** = a basic version exists, **TODO** = you build it.

Before choosing a task, claim one primary app in the team task board using `docs/APP_OWNERSHIP.md`. Coordinate cross-app changes with the affected owner. For new and updated endpoints, use function-based views and permission helpers; do not add class-based views or mixins. Existing starter view scaffolding is legacy and is not an example for new work.

Unfinished pages have starter placeholder endpoints. Treat existing class-based view scaffolding as legacy; implement new or updated endpoints as function-based views and follow `docs/HOW_TO_BUILD_A_PAGE.md`.

| ID | Task | Owner | Hours | State | Where to work |
|---|---|---|---|---|---|
| **Sprint 0 - Setup** | | | | | |
| LMS-001 | Create GitHub repo, branch protection (main/develop), .gitignore, README | PM | 1 | TODO | You (PM): create the GitHub repo and push this starter. See README > 'Put it on GitHub'. |
| LMS-002 | Create Django project 'config' with split settings (base/dev/prod), django-environ, .env.example | BE-1 | 3 | DONE | config/settings/ (base, dev, prod), .env.example |
| LMS-003 | Configure the local database | BE-3 | 2 | DONE | SQLite is the local default; Docker/PostgreSQL are out of scope for now |
| LMS-004 | Create the 6 apps (core, accounts, courses, enrollments, assessments, attendance) and register them | BE-1 | 1 | DONE | All 6 apps exist and are registered in config/settings/base.py |
| LMS-005 | Base template: Bootstrap 5, navbar that changes per role, messages and pagination partials | FE | 4 | STARTER | templates/base.html, partials/navbar.html, static/css/app.css. Basic version done - FE to polish. |
| LMS-006 | Add ruff/black, pre-commit and a GitHub Actions workflow that runs tests on every PR | BE-2 | 3 | DONE | .github/workflows/ci.yml, .pre-commit-config.yaml, pyproject.toml (ruff) |
| LMS-007 | Create Slack channels, connect GitHub app, build the standup workflow and task board (see Slack section) | PM | 2 | TODO | You (PM): Slack channels, GitHub app, standup workflow, task board |
| LMS-008 | Set up pytest + factory-boy and write the test-case checklist for workflows A to E | QA | 5 | STARTER | pytest is set up (tests/conftest.py has fixtures). QA still writes the test-case checklist. |
| **Sprint 1 - Accounts and Roles** | | | | | |
| LMS-101 | Custom User model (role, phone, photo) - MUST be done before the first migrate | BE-1 | 3 | DONE | accounts/models.py (User) |
| LMS-102 | FacilitatorProfile and StudentProfile models + signal that creates the profile automatically | BE-1 | 3 | DONE | accounts/models.py (profiles), accounts/signals.py |
| LMS-103 | Student registration, login, logout and password reset (views + templates) | BE-3 | 6 | STARTER | Register, login, logout work (accounts/views.py, templates/registration, templates/accounts/register.html). TODO: password reset (4 pages + email), more tests. |
| LMS-104 | Shared role and object permission rules | BE-1 | 4 | STARTER | core/permissions.py, tests/test_permissions.py; use function-based view permission helpers |
| LMS-105 | Admin user management: list, create facilitator, edit, activate/deactivate | BE-2 | 6 | TODO | accounts/views.py (function handlers), accounts/forms.py, templates/accounts/user_*.html |
| LMS-106 | Admin facilitator list with grant / revoke 'can_manage_courses' button | BE-2 | 4 | TODO | accounts/views.py (function handlers), templates/accounts/facilitator_list.html. Model methods grant_course_rights() / revoke_course_rights() already exist. |
| LMS-107 | Profile view and edit pages for all roles | FE | 4 | TODO | accounts/views.py (function handlers), accounts/forms.py, templates/accounts/profile_form.html |
| LMS-108 | Dashboard redirect by role + three placeholder dashboards | BE-3 | 3 | DONE | core/views.py, templates/core/ |
| LMS-109 | Write tests: registration, login, access rules, grant/revoke right | QA | 6 | TODO | tests/test_permissions.py and tests/test_models.py - extend them |
| LMS-110 | Management command create_demo_data (admin, facilitators, students, courses) | BE-3 | 3 | DONE | core/management/commands/create_demo_data.py  ->  python manage.py create_demo_data |
| LMS-111 | Static HTML prototypes (home, course detail, dashboards) so pages are designed before the views exist | FE | 8 | TODO | New folder prototypes/ (plain HTML + Bootstrap). No Django needed. |
| **Sprint 2 - Courses, Units and Home Page** | | | | | |
| LMS-201 | Course model, admin registration and migrations | BE-2 | 3 | DONE | courses/models.py (Course), courses/admin.py |
| LMS-202 | Unit model with facilitator FK and ordering | BE-3 | 2 | DONE | courses/models.py (Unit) |
| LMS-203 | Course create / update / delete views with ownership checks | BE-2 | 8 | TODO | courses/views.py (function handlers), courses/forms.py, templates/courses/course_form.html |
| LMS-204 | Course form validation (dates, capacity) and image upload | BE-3 | 3 | TODO | courses/forms.py (CourseForm validation) |
| LMS-205 | Publish / close course action (status change) | BE-3 | 2 | TODO | courses/views.py (function handler), courses/services.py |
| LMS-206 | Unit CRUD nested under a course + assign facilitator to unit | BE-1 | 6 | TODO | courses/views.py (function handlers), courses/forms.py, templates/courses/unit_*.html |
| LMS-207 | Home page: published course cards, search, filter, pagination | FE | 8 | STARTER | core/views.py + templates/core/home.html. Basic list + search done. TODO: filters, design. |
| LMS-208 | Course detail page with unit list and smart 'Apply' button state | FE | 5 | STARTER | courses/views.py + templates/courses/course_detail.html. Works. TODO: polish. |
| LMS-209 | 'Manage courses' table page for admin and course managers | FE | 4 | TODO | courses/views.py (function handler), templates/courses/course_manage_list.html |
| LMS-210 | 'My units' page for facilitators (units I teach) | BE-1 | 3 | TODO | courses/views.py (function handler), templates/courses/my_units.html (selector already exists) |
| LMS-211 | Tests: who can create / edit / delete, unpublished courses hidden from home | QA | 8 | TODO | tests/test_courses.py (new file) |
| **Sprint 3 - Applications and Enrollment** | | | | | |
| LMS-301 | Application model with unique (student, course) constraint | BE-3 | 2 | DONE | enrollments/models.py (Application) |
| LMS-302 | Enrollment model | BE-3 | 2 | DONE | enrollments/models.py (Enrollment) |
| LMS-303 | Apply view + form; rules: window open, capacity, no duplicates | BE-2 | 5 | TODO | enrollments/views.py (function handler), enrollments/forms.py, enrollments/services.py |
| LMS-304 | 'My applications' page with withdraw button | FE | 4 | TODO | enrollments/views.py (function handlers), templates/enrollments/my_applications.html |
| LMS-305 | Manage applications list with filters (status, course) | BE-3 | 5 | TODO | enrollments/views.py (function handlers), django-filter |
| LMS-306 | Approve / reject with note; service function creates Enrollment | BE-1 | 5 | TODO | enrollments/services.py (approve_application, reject_application), enrollments/views.py (function handlers) |
| LMS-307 | Email on decision (console backend in dev, SMTP in prod) | BE-3 | 3 | TODO | enrollments/services.py (send_mail on decision) |
| LMS-308 | Student 'My courses' page + facilitator unit roster | FE | 5 | TODO | enrollments/views.py (function handlers), templates/enrollments/ |
| LMS-309 | Tests: apply rules, approval flow, capacity edge cases | QA | 6 | TODO | tests/test_enrollments.py (new file) |
| **Sprint 4 - Assessments and Feedback** | | | | | |
| LMS-401 | Test, TestResult and Feedback models | BE-3 | 4 | DONE | assessments/models.py |
| LMS-402 | Test CRUD for the unit's facilitator | BE-2 | 6 | TODO | assessments/views.py (function handlers), assessments/forms.py, templates/assessments/test_*.html |
| LMS-403 | Bulk marks entry page (formset for all enrolled students) | BE-3 | 8 | TODO | assessments/views.py (function handler), assessments/services.py, templates/assessments/marks_entry.html |
| LMS-404 | Feedback create / update form linked to a result | BE-1 | 5 | TODO | assessments/views.py (function handler), assessments/forms.py, assessments/services.py |
| LMS-405 | Student results list and result detail with feedback | FE | 6 | TODO | assessments/views.py (function handlers), templates/assessments/my_results.html, result_detail.html |
| LMS-406 | Facilitator 'pending feedback' filter | BE-2 | 3 | TODO | assessments/selectors.py (results_pending_feedback already written) + a facilitator page |
| LMS-407 | In-app notification when feedback is added (optional) | BE-1 | 4 | TODO | Optional. Needs a small Notification model (not in the starter) - discuss with the lead first. |
| LMS-408 | Tests: marks validation, feedback permissions, student privacy | QA | 6 | TODO | tests/test_assessments.py (new file) |
| **Sprint 5 - Attendance** | | | | | |
| LMS-501 | ClassSession and AttendanceRecord models | BE-1 | 3 | DONE | attendance/models.py |
| LMS-502 | Session CRUD for the unit's facilitator | BE-1 | 5 | TODO | attendance/views.py (function handlers), attendance/forms.py, templates/attendance/session_*.html |
| LMS-503 | Mark-attendance page (status per student, 'mark all present') | BE-1 | 8 | TODO | attendance/views.py (function handler), attendance/services.py, templates/attendance/mark_attendance.html |
| LMS-504 | Unit attendance report: % per student, highlight low attendance | BE-3 | 6 | TODO | attendance/views.py (function handler), attendance/services.py |
| LMS-505 | Export attendance to CSV / PDF | BE-3 | 4 | TODO | attendance/views.py (function handler) |
| LMS-506 | Student 'My attendance' page | FE | 4 | TODO | attendance/views.py (function handler), templates/attendance/my_attendance.html |
| LMS-507 | Admin attendance overview across all units | BE-2 | 4 | TODO | attendance/views.py (function handler) |
| LMS-508 | Tests: only unit facilitator can mark, no duplicate records | QA | 5 | TODO | tests/test_attendance.py (new file) |
| **Sprint 6 - Dashboards, Polish and Release** | | | | | |
| LMS-601 | Admin dashboard: totals, pending applications, recent activity | BE-2 | 6 | TODO | core/views.py (function handler), templates/core/dashboard_admin.html |
| LMS-602 | Facilitator dashboard: my units, upcoming sessions, pending feedback | BE-1 | 5 | TODO | core/views.py (function handler), templates/core/dashboard_facilitator.html |
| LMS-603 | Student dashboard: my courses, next sessions, latest results, attendance % | BE-3 | 5 | TODO | core/views.py (function handler), templates/core/dashboard_student.html |
| LMS-604 | UI polish: responsive check, empty states, 403/404/500 pages | FE | 8 | TODO | templates/ and static/css/app.css |
| LMS-605 | Performance pass: select_related / prefetch_related, indexes, pagination | BE-2 | 4 | TODO | Whole project: select_related / prefetch_related, indexes |
| LMS-606 | Security review using the checklist in this document | BE-1 | 4 | TODO | Review against the security checklist in the plan PDF (section 10.2) |
| LMS-607 | Full regression + user acceptance testing with real users | QA | 12 | TODO | Manual testing with real users + regression |
| LMS-608 | Production settings, Gunicorn + Nginx / Whitenoise, env vars, DB backups | BE-2 | 8 | TODO | config/settings/prod.py, requirements/prod.txt, server setup |
| LMS-609 | Deploy, smoke test, hand-over documentation and training | PM | 6 | TODO | Deployment and hand-over |
