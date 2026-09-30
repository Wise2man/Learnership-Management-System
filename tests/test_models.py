import pytest
from django.db import IntegrityError, transaction

from accounts.models import FacilitatorProfile, StudentProfile, User
from courses.models import Course
from enrollments.models import Application


def test_student_gets_profile_and_number(student):
    assert StudentProfile.objects.filter(user=student).exists()
    assert student.student_profile.student_number.startswith("STU-")


def test_facilitator_gets_profile_without_course_right(facilitator):
    assert FacilitatorProfile.objects.filter(user=facilitator).exists()
    assert facilitator.can_manage_courses is False


def test_grant_and_revoke_course_right(facilitator, admin_user):
    facilitator.facilitator_profile.grant_course_rights(admin_user)
    facilitator.refresh_from_db()
    assert User.objects.get(pk=facilitator.pk).can_manage_courses is True
    assert facilitator.facilitator_profile.granted_by == admin_user
    facilitator.facilitator_profile.revoke_course_rights(admin_user)
    assert User.objects.get(pk=facilitator.pk).can_manage_courses is False


def test_admin_can_always_manage_courses_student_never(admin_user, student):
    assert admin_user.can_manage_courses is True
    assert student.can_manage_courses is False


def test_superuser_is_forced_to_admin_role(db):
    user = User.objects.create_superuser("root", "root@example.com", "Password123!")
    assert user.role == User.Role.ADMIN


def test_course_slug_is_unique_and_never_reserved(course, course_manager):
    kwargs = dict(
        description="x",
        created_by=course_manager,
        application_open=course.application_open,
        application_close=course.application_close,
        start_date=course.start_date,
        end_date=course.end_date,
    )
    same_title = Course.objects.create(title="Test Course", **kwargs)
    assert same_title.slug != course.slug
    reserved = Course.objects.create(title="Create", **kwargs)
    assert reserved.slug not in Course.RESERVED_SLUGS


def test_only_one_application_per_student_per_course(student, course):
    Application.objects.create(student=student, course=course, motivation="x" * 40)
    with pytest.raises(IntegrityError), transaction.atomic():
        Application.objects.create(student=student, course=course, motivation="again")


def test_home_queryset_only_has_published_open_courses(course, course_manager):
    Course.objects.create(
        title="Hidden draft",
        description="x",
        status="DRAFT",
        created_by=course_manager,
        application_open=course.application_open,
        application_close=course.application_close,
        start_date=course.start_date,
        end_date=course.end_date,
    )
    titles = list(Course.objects.on_home_page().values_list("title", flat=True))
    assert titles == ["Test Course"]
