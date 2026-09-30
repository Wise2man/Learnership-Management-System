# Learnership Management System (LMS)

A Django web app where **students apply for learnerships/courses**, **facilitators** run them
(units, tests, feedback, attendance) and an **admin** controls everything.

| Role | Can do |
|---|---|
| Student | See published courses on the home page, apply, see own results, feedback and attendance |
| Facilitator | Teach units, enter marks, give feedback, take attendance. If the admin grants the **course right**, also create / edit / delete their own courses |
| Admin | Almost everything, including granting or removing the course right |

> Read first: `docs/planning/Team_Guide_How_We_Work.pdf` (how we work) and
> `docs/planning/Learnership_Management_System_Plan.pdf` (the full plan).
> Your tasks and the files to work in: `docs/TASK_MAP.md`.

---

## 1. Start in 5 minutes

You need **Python 3.12** and **Git**. Development uses SQLite; Docker is not part of the current setup.

```bash
git clone https://github.com/Wise2man/Learnership-Management-System.git
cd learnership_lms

python -m venv venv
source venv/bin/activate          # Windows:  venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env              # Windows:  copy .env.example .env
python manage.py migrate
python manage.py create_demo_data # fake users, courses, marks, attendance
python manage.py runserver
```

Open <http://127.0.0.1:8000/>.

**Demo logins** (password for all: `Password123!`)

| Username | Role |
|---|---|
| `admin1` | Admin |
| `fac_manager` | Facilitator **with** the course right |
| `fac_plain` | Facilitator **without** the course right |
| `student1` ... `student5` | Students (1-3 are enrolled, 4-5 have a pending application) |

By default the app uses **SQLite** (a file), so nothing else is needed.

PostgreSQL is out of scope for the current local setup. Keep `DATABASE_URL` unset to use SQLite.

---

## 2. Everyday commands

| Command | What it does |
|---|---|
| `make run` | Start the server |
| `make test` | Run all tests |
| `make migrations` then `make migrate` | After you change a model |
| `make format` | Fix code style automatically |
| `make check` | **Run before every Pull Request**: style, migrations, tests |
| `make demo` | Reset demo data |

No `make` on Windows? Run the command inside the Makefile directly (e.g. `pytest`, `ruff check .`).

Install the commit checker once: `pre-commit install`

---

## 3. What is in the project

```
config/            settings (base, dev, prod), root urls
core/              shared pages, permission rules, demo data command
accounts/          User (role), FacilitatorProfile (course right), StudentProfile, register / login
courses/           Course, Unit
enrollments/       Application, Enrollment
assessments/       Test, TestResult, Feedback
attendance/        ClassSession, AttendanceRecord
templates/         base.html + one folder per app
static/            css / js / img
tests/             pytest tests (permission tests are the most important)
docs/              task map, architecture, how-to guides, planning PDFs
```

Inside each app: `models.py forms.py views.py urls.py services.py selectors.py admin.py`.

Each developer claims one app before starting work; see `docs/APP_OWNERSHIP.md`.

* **Business rules** go in `services.py` (e.g. `approve_application()`), not in views.
* **Reusable queries** go in `selectors.py`.
* **New and updated views** use Django function-based views and permission decorators/helpers, not class-based views or mixins.

### What is already built vs. what you build

* Built: models + migrations, admin site, settings, register/login/logout, role-based navbar,
  home page (search + pagination), course detail, demo data, and CI.
* The starter also contains *"Not built yet"* placeholder endpoints. Existing view scaffolding uses
  class-based views and mixins; treat it as legacy. New or updated endpoints must use function-based
  views and shared permission helpers, as described in `docs/APP_OWNERSHIP.md`.
  Step by step: **`docs/HOW_TO_BUILD_A_PAGE.md`**.

---

## 4. How we use Git

```bash
git checkout develop && git pull
git checkout -b feature/LMS-203-course-crud
# ... work, then:
make check
git add . && git commit -m "LMS-203: add course create view"
git push -u origin feature/LMS-203-course-crud
# open a Pull Request into `develop`, ask the lead to review
```

Rules: never push straight to `main` or `develop`; one branch per task; one approval before merge;
CI must be green. Details: `docs/GIT_WORKFLOW.md` and `CONTRIBUTING.md`.

---

## 5. Put it on GitHub (lead does this once)

```bash
cd learnership_lms
git init -b main
git add .
git commit -m "LMS-001: starter project"
git remote add origin https://github.com/Wise2man/Learnership-Management-System.git
git push -u origin main
git checkout -b develop && git push -u origin develop
```

Then on GitHub: **Settings > Branches**: protect `main` and `develop` (require a Pull Request,
1 approval, and the `CI / test` check). Set `develop` as the default branch. Invite the team.

---

## 6. Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError` | Activate the virtual environment, then `pip install -r requirements.txt` |
| `no such table` / missing column | `python manage.py migrate` |
| Two migrations clash after a merge | `python manage.py makemigrations --merge`, tell the team |
| Page shows *Not built yet* | That is a placeholder. See `docs/TASK_MAP.md` |
| `403` on a page | You are logged in as the wrong role. Use the demo logins above |
| CSS looks unstyled | Bootstrap loads from a CDN, so you need internet access |
