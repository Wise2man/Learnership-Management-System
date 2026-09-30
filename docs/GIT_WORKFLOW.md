# Git workflow

```
main       production code only. Updated by the lead when we release.
develop    integration branch. All finished work is merged here.
feature/*  one branch per task, always created from develop.
```

## Naming
* Branch: `feature/LMS-203-course-crud`
* Commit: `LMS-203: add course create view`
* Pull Request title: `LMS-203: Course create / edit / delete views`

## Keeping your branch fresh
```bash
git checkout develop && git pull
git checkout feature/LMS-203-course-crud
git merge develop        # fix conflicts if any, then run: make check
```

## Migrations (the most common conflict)
* Only the **owner of an app** changes that app's models. Ask first if you need a change.
* If two migration files use the same number after a merge:
  ```bash
  python manage.py makemigrations --merge
  ```
  Tell the team in `#lms-backend`.
* Never edit or delete a migration that is already on `develop`.

## Branch protection (GitHub > Settings > Branches)
For `main` and `develop`: require a Pull Request, require 1 approval, require the `CI / test` check, block force-push.
