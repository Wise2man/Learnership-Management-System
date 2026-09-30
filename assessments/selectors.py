"""Reusable queries for tests and results."""

from .models import TestResult


def results_for_student(user):
    """A student may only ever see THEIR OWN results."""
    return TestResult.objects.filter(student=user).select_related("test", "test__unit", "feedback")


def results_pending_feedback(facilitator):
    """LMS-406: marked results of the facilitator's units that have no feedback yet."""
    return TestResult.objects.filter(
        test__unit__facilitator=facilitator, status=TestResult.Status.MARKED, feedback__isnull=True
    ).select_related("student", "test")
