"""Reusable queries for applications and enrollments."""

from .models import Application, Enrollment


def applications_for_reviewer(user):
    """Admin: all applications. Course manager: applications for courses they created."""
    qs = Application.objects.select_related("student", "course")
    if user.is_admin_role:
        return qs
    return qs.filter(course__created_by=user)


def active_students_for_unit(unit):
    """Students with an ACTIVE enrollment in the unit's course (roster for tests and attendance)."""
    return (
        Enrollment.objects.filter(course=unit.course, status=Enrollment.Status.ACTIVE)
        .select_related("student")
        .order_by("student__first_name", "student__last_name")
    )
