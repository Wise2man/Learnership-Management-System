from django.shortcuts import get_object_or_404

from core.mixins import StudentRequiredMixin, UnitFacilitatorRequiredMixin
from core.views import PlaceholderView

from .models import Test, TestResult


class TestUnitMixin(UnitFacilitatorRequiredMixin):
    """For URLs like /tests/<pk>/ : the unit comes from the Test."""

    def get_unit(self):
        return get_object_or_404(Test, pk=self.kwargs["pk"]).unit


class ResultUnitMixin(UnitFacilitatorRequiredMixin):
    """For URLs like /results/<pk>/feedback/ : the unit comes from the TestResult."""

    def get_unit(self):
        return get_object_or_404(TestResult, pk=self.kwargs["pk"]).test.unit


class TestListView(UnitFacilitatorRequiredMixin, PlaceholderView):
    task_id = "LMS-402"
    page_title = "Tests for this unit"


class TestCreateView(UnitFacilitatorRequiredMixin, PlaceholderView):
    task_id = "LMS-402"
    page_title = "Create test"
    hint = "Set unit = self.unit and created_by = request.user."


class TestDetailView(TestUnitMixin, PlaceholderView):
    task_id = "LMS-402"
    page_title = "Test details and marks"


class TestUpdateView(TestUnitMixin, PlaceholderView):
    task_id = "LMS-402"
    page_title = "Edit test"


class TestDeleteView(TestUnitMixin, PlaceholderView):
    task_id = "LMS-402"
    page_title = "Delete test"


class MarksEntryView(TestUnitMixin, PlaceholderView):
    task_id = "LMS-403"
    page_title = "Enter marks"
    hint = "A formset with one row per ACTIVE student. Use assessments.services.save_marks()."


class FeedbackFormView(ResultUnitMixin, PlaceholderView):
    task_id = "LMS-404"
    page_title = "Give feedback"
    hint = "Create or update the Feedback for this TestResult."


class StudentResultListView(StudentRequiredMixin, PlaceholderView):
    task_id = "LMS-405"
    page_title = "My results"
    hint = "Use assessments.selectors.results_for_student(request.user)."


class StudentResultDetailView(StudentRequiredMixin, PlaceholderView):
    task_id = "LMS-405"
    page_title = "Result details"
    hint = "Object-level check! Query with student=request.user so other students get 404. Write a test."
