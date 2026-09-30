"""Reusable queries for sessions and attendance."""

from .models import AttendanceRecord


def records_for_student(user):
    """A student may only ever see THEIR OWN attendance."""
    return AttendanceRecord.objects.filter(student=user).select_related("session", "session__unit")
