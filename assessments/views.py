"""
Assessments views.

This app handles:
- Tests
- Student test results / marks
- Facilitator feedback
"""

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from courses.models import Unit
from .models import Test, TestResult


# ============================================================
# TEST VIEWS
# ============================================================

def test_list_view(request, unit_pk):
    """
    Display all tests belonging to a specific unit.
    """

    # Get the Unit using the unit_pk from the URL.
    unit = get_object_or_404(Unit, pk=unit_pk)

    # Get all tests belonging to this unit.
    tests = Test.objects.filter(unit=unit)

    # Render the test list page.
    return render(
        request,
        "assessments/test_list.html",
        {
            "unit": unit,
            "tests": tests,
        },
    )


def test_create_view(request, unit_pk):
    """
    Create a new test for a unit.

    The test should be linked to:
    - the selected Unit
    - the logged-in facilitator through created_by
    """

    # TODO:
    # Handle POST request and create the Test.
    #
    # Example:
    #
    # Test.objects.create(
    #     unit=unit,
    #     title=...,
    #     description=...,
    #     total_marks=...,
    #     pass_mark=...,
    #     test_date=...,
    #     created_by=request.user,
    # )

    # Temporary response while the create functionality
    # is being implemented.
    return HttpResponse("Test create view is working.")


def test_detail_view(request, pk):
    """
    Display the details of one test.

    The primary key (pk) identifies the Test.
    """

    # Retrieve the test from the database.
    # If the test does not exist, Django returns a 404 response.
    test = get_object_or_404(Test, pk=pk)

    # Get the Unit that this test belongs to.
    unit = test.unit

    # Get all student results for this test.
    results = test.objects.all()

    # Render the test detail page.
    return render(
        request,
        "assessments/test_detail.html",
        {
            "test": test,
            "unit": unit,
            "results": results,
        },
    )


def test_update_view(request, pk):
    """
    Edit an existing test.

    The pk identifies the test that will be edited.
    """

    # Retrieve the test.
    test = get_object_or_404(Test, pk=pk)

    # Get the Unit associated with the test.
    unit = test.unit

    # TODO:
    # Handle POST request and update:
    # - title
    # - description
    # - total_marks
    # - pass_mark
    # - test_date

    # Render the test form.
    return render(
        request,
        "assessments/test_form.html",
        {
            "test": test,
            "unit": unit,
        },
    )


def test_delete_view(request, pk):
    """
    Delete an existing test.

    Deleting a Test will also delete its TestResults because
    TestResult.test uses on_delete=models.CASCADE.
    """

    # Retrieve the test that will be deleted.
    test = get_object_or_404(Test, pk=pk)

    # Get the Unit associated with the test.
    unit = test.unit

    # TODO:
    # Only delete the test after the user confirms the action.

    # Render the confirmation page.
    return render(
        request,
        "assessments/test_confirm_delete.html",
        {
            "test": test,
            "unit": unit,
        },
    )


# ============================================================
# MARKS / TEST RESULTS
# ============================================================

def marks_entry_view(request, pk):
    """
    Enter marks for students who completed a test.

    One TestResult represents one student's mark for one Test.
    """

    # Retrieve the test.
    test = get_object_or_404(Test, pk=pk)

    # Get the Unit associated with the test.
    unit = test.unit

    # Get existing results for this test.
    results = test.objects.all()

    # TODO:
    # Create a formset with one row per ACTIVE student.
    #
    # Each row should create or update a TestResult.
    #
    # Marks should be saved using:
    # assessments.services.save_marks()
    #
    # The service should handle:
    # - marks_obtained
    # - status
    # - marked_by
    # - marked_at

    # Render the marks entry page.
    return render(
        request,
        "assessments/marks_entry.html",
        {
            "test": test,
            "unit": unit,
            "results": results,
        },
    )


# ============================================================
# FEEDBACK
# ============================================================

def feedback_form_view(request, pk):
    """
    Give feedback for one student's test result.

    Feedback belongs to a TestResult through a OneToOneField.
    """

    # Retrieve the student's TestResult.
    result = get_object_or_404(TestResult, pk=pk)

    # Get the Unit through:
    #
    # TestResult -> Test -> Unit
    #
    unit = result.test.unit

    # Check whether feedback already exists.
    #
    # Because Feedback.result is a OneToOneField, each result
    # can have only one Feedback object.
    feedback = getattr(result, "feedback", None)

    # TODO:
    # On POST:
    # - create Feedback if it doesn't exist
    # - update Feedback if it already exists
    #
    # facilitator should be request.user
    #
    # Example:
    #
    # Feedback.objects.update_or_create(
    #     result=result,
    #     defaults={
    #         "facilitator": request.user,
    #         "comment": comment,
    #         "areas_for_improvement": areas_for_improvement,
    #     },
    # )

    # Render the feedback form.
    return render(
        request,
        "assessments/feedback_form.html",
        {
            "result": result,
            "unit": unit,
            "feedback": feedback,
        },
    )


# ============================================================
# STUDENT RESULTS
# ============================================================

def student_result_list_view(request):
    """
    Display all test results belonging to the logged-in student.
    """

    # TODO:
    # Retrieve only results belonging to the current user.
    #
    # Example:
    #
    # results = TestResult.objects.filter(
    #     student=request.user
    # )

    # Render the student results page.
    return render(
        request,
        "assessments/student_results.html",
        {
            # "results": results,
        },
    )


def student_result_detail_view(request, pk):
    """
    Display details of one test result.

    The result is filtered by both:
    - pk
    - request.user

    This prevents a student from viewing another student's
    result by manually changing the ID in the URL.
    """

    # Retrieve the result only if it belongs to the
    # currently logged-in student.
    #
    # If the result belongs to another student,
    # Django returns a 404 response.
    result = get_object_or_404(
        TestResult,
        pk=pk,
        student=request.user,
    )

    # Get the associated test.
    test = result.test

    # Get the unit through the test.
    unit = test.unit

    # Get feedback if it exists.
    feedback = getattr(result, "feedback", None)

    # Render the result detail page.
    return render(
        request,
        "assessments/student_result_detail.html",
        {
            "result": result,
            "test": test,
            "unit": unit,
            "feedback": feedback,
        },
    )
