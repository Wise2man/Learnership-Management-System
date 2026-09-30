from datetime import date, timedelta

import pytest
from django.test import Client

from accounts.models import User
from courses.models import Course, Unit

PASSWORD = "Password123!"


def _make_user(username, role, **extra):
    return User.objects.create_user(username, f"{username}@example.com", PASSWORD, role=role, **extra)


@pytest.fixture
def admin_user(db):
    return _make_user("admin1", "ADMIN")


@pytest.fixture
def student(db):
    return _make_user("student1", "STUDENT")


@pytest.fixture
def other_student(db):
    return _make_user("student2", "STUDENT")


@pytest.fixture
def facilitator(db):
    """A facilitator WITHOUT the course right."""
    return _make_user("fac_plain", "FACILITATOR")


@pytest.fixture
def other_facilitator(db):
    return _make_user("fac_other", "FACILITATOR")


@pytest.fixture
def course_manager(db, admin_user):
    """A facilitator WITH the course right."""
    user = _make_user("fac_manager", "FACILITATOR")
    user.facilitator_profile.grant_course_rights(admin_user)
    return user


@pytest.fixture
def other_course_manager(db, admin_user):
    user = _make_user("fac_manager2", "FACILITATOR")
    user.facilitator_profile.grant_course_rights(admin_user)
    return user


@pytest.fixture
def course(db, course_manager):
    today = date.today()
    return Course.objects.create(
        title="Test Course",
        description="A course for tests",
        status=Course.Status.PUBLISHED,
        created_by=course_manager,
        application_open=today - timedelta(days=1),
        application_close=today + timedelta(days=30),
        start_date=today + timedelta(days=40),
        end_date=today + timedelta(days=400),
        capacity=2,
    )


@pytest.fixture
def unit(db, course, facilitator):
    return Unit.objects.create(course=course, title="Unit One", order=1, facilitator=facilitator)


@pytest.fixture
def login():
    """Usage: client = login(user)"""

    def _login(user):
        client = Client()
        client.force_login(user)
        return client

    return _login
