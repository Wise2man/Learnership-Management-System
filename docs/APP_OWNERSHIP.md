# App ownership

Each developer chooses one app as their primary area before taking a task. Claim it in the team task board and add your name beside the app there. Do not assume an app is unowned: coordinate with its current owner first. App ownership helps route reviews; it does not prevent other developers from contributing.

| App | Responsibility | Initial owner |
|---|---|---|
| accounts | Users, roles, profiles, authentication | Unclaimed |
| courses | Courses, units, publishing, course discovery | Unclaimed |
| enrollments | Applications, decisions, and learner enrollment | Unclaimed |
| assessments | Tests, results, and learner feedback | Unclaimed |
| attendance | Class sessions, attendance records, and reports | Unclaimed |
| core | Shared home pages, dashboards, permissions, and shared utilities | Unclaimed |

## App structure

Keep app-specific code together:

```text
<app>/
  models.py       data owned by the app
  forms.py        app forms and validation
  views.py        function-based request handlers
  urls.py         app URL patterns
  services.py     business operations and state changes
  selectors.py    reusable read/query operations
  admin.py        Django admin registration
  migrations/     schema history
templates/<app>/  app templates
tests/            shared tests, grouped by app (test_<app>.py)
```

An app owns its models and migrations. For changes that cross app boundaries, discuss the contract with each affected owner before editing another app's models or migrations. Keep permission decisions on the server and cover them with tests.

## View convention

New and updated request handlers are Django function-based views. Use shared permission functions/decorators; do not add class-based views or mixins. Keep request handling in `views.py`, business rules in `services.py`, and reusable queries in `selectors.py`. Mutations must use POST and protect against CSRF.

The starter currently contains class-based views and mixins. They are legacy scaffold, not the pattern for new work; converting existing endpoints is a separate task so app features are not silently changed during setup.

## Local development

Use the default SQLite database. Docker and PostgreSQL are not part of the current development setup.