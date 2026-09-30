"""
Permission rules in ONE place. Mixins, views and templates all use these functions,
so a rule is written once and tested once.
"""


def can_manage_courses(user):
    return user.is_authenticated and user.can_manage_courses


def can_edit_course(user, course):
    """Admin can edit any course. A facilitator with the right can edit only their own."""
    if not user.is_authenticated:
        return False
    if user.is_admin_role:
        return True
    return user.can_manage_courses and course.created_by_id == user.id


def can_review_applications(user, course):
    return can_edit_course(user, course)


def can_teach_unit(user, unit):
    """Admin, or the facilitator assigned to this unit."""
    if not user.is_authenticated:
        return False
    if user.is_admin_role:
        return True
    return user.is_facilitator and unit.facilitator_id == user.id
