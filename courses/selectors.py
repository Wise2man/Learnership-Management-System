"""Reusable queries for courses and units."""

from .models import Course, Unit


def courses_for_manager(user):
    """Admin sees all courses; a course manager sees the ones they created."""
    if user.is_admin_role:
        return Course.objects.all()
    return Course.objects.filter(created_by=user)


def units_for_facilitator(user):
    """Units a facilitator teaches (Admin: all units)."""
    qs = Unit.objects.select_related("course", "facilitator")
    if user.is_admin_role:
        return qs
    return qs.filter(facilitator=user)
