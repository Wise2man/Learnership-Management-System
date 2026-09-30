# How to build a page (replace a placeholder)

Use this guide with `docs/APP_OWNERSHIP.md` and the task map. The starter includes class-based placeholder endpoints; new or updated work should use function-based views and must not introduce mixins.

## Build workflow

1. Claim the owning app and task before editing.
2. Trace the app URL name and current route in its `urls.py`; preserve the public URL unless the task requires a change.
3. Put request handling in the app's `views.py`, validation in `forms.py`, business operations in `services.py`, and reusable reads in `selectors.py`.
4. Enforce authorization on the server with the shared permission helpers. Scope data by the current user or assigned unit, not only by hiding template links.
5. Put templates under `templates/<app>/`. Include CSRF protection on forms that change data; state changes must not happen on GET.
6. Add app-focused tests for success, invalid input, permissions, and object-level access. Keep shared tests in `tests/test_<app>.py`.
7. Run `make check`, then open a pull request using the task ID and request review from the app owner.

## Before review

- The endpoint is a function-based view and uses no mixins.
- Permission and object-ownership checks are enforced server-side and tested.
- Forms have useful validation; pages include empty and error states.
- Templates use named URLs and render at phone-sized widths.
- `make check` passes.
