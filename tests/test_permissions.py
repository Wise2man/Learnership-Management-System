"""
PERMISSION TESTS - the most important tests in the project.
Every new view must be added to one of the tables below.
"""

import pytest
from django.urls import reverse

# --- who may open what -----------------------------------------------------
# Each row: (url_name, kwargs-builder, {role_fixture: expected_status})
# 200 = allowed, 403 = logged in but not allowed, 302 = redirected (anonymous -> login)

ADMIN_ONLY = ["accounts:user_list", "accounts:user_create", "accounts:fac_list", "attendance:overview"]
COURSE_MANAGER = ["courses:manage", "courses:create", "enrollments:app_list"]
STUDENT_ONLY = ["enrollments:my_apps", "enrollments:my_courses", "assessments:my_results", "attendance:my_attendance"]


@pytest.mark.parametrize("name", ADMIN_ONLY)
def test_admin_only_pages(name, client, login, admin_user, course_manager, student):
    assert client.get(reverse(name)).status_code == 302  # anonymous -> login
    assert login(student).get(reverse(name)).status_code == 403
    assert login(course_manager).get(reverse(name)).status_code == 403
    assert login(admin_user).get(reverse(name)).status_code == 200


@pytest.mark.parametrize("name", COURSE_MANAGER)
def test_course_manager_pages(name, client, login, admin_user, course_manager, facilitator, student):
    assert client.get(reverse(name)).status_code == 302
    assert login(student).get(reverse(name)).status_code == 403
    assert login(facilitator).get(reverse(name)).status_code == 403  # facilitator WITHOUT the right
    assert login(course_manager).get(reverse(name)).status_code == 200
    assert login(admin_user).get(reverse(name)).status_code == 200


@pytest.mark.parametrize("name", STUDENT_ONLY)
def test_student_only_pages(name, client, login, admin_user, facilitator, student):
    assert client.get(reverse(name)).status_code == 302
    assert login(facilitator).get(reverse(name)).status_code == 403
    assert login(admin_user).get(reverse(name)).status_code == 403
    assert login(student).get(reverse(name)).status_code == 200


def test_my_units_is_for_facilitators_and_admin(client, login, admin_user, facilitator, student):
    url = reverse("courses:my_units")
    assert client.get(url).status_code == 302
    assert login(student).get(url).status_code == 403
    assert login(facilitator).get(url).status_code == 200
    assert login(admin_user).get(url).status_code == 200


# --- course ownership ---------------------------------------------------------
def test_only_owner_or_admin_can_edit_a_course(
    login, course, course_manager, other_course_manager, admin_user, facilitator
):
    url = reverse("courses:edit", kwargs={"slug": course.slug})
    assert login(course_manager).get(url).status_code == 200  # owner
    assert login(admin_user).get(url).status_code == 200  # admin can edit any
    assert login(other_course_manager).get(url).status_code == 403  # has the right, but NOT the owner
    assert login(facilitator).get(url).status_code == 403  # no right at all


# --- unit facilitator rules ---------------------------------------------------
def test_only_unit_facilitator_or_admin_can_open_unit_pages(
    login, unit, facilitator, other_facilitator, admin_user, student
):
    for name in ["assessments:test_list", "attendance:session_list", "attendance:report", "enrollments:roster"]:
        url = reverse(name, kwargs={"unit_pk": unit.pk})
        assert login(facilitator).get(url).status_code == 200, name
        assert login(admin_user).get(url).status_code == 200, name
        assert login(other_facilitator).get(url).status_code == 403, name
        assert login(student).get(url).status_code == 403, name


def test_grant_right_makes_menu_link_appear(login, facilitator, admin_user):
    client = login(facilitator)
    assert "Manage courses" not in client.get(reverse("core:dash_fac")).content.decode()
    facilitator.facilitator_profile.grant_course_rights(admin_user)
    assert "Manage courses" in login(facilitator).get(reverse("core:dash_fac")).content.decode()
