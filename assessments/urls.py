from django.urls import path

from . import views


urlpatterns = [
    # ============================================================
    # TESTS
    # ============================================================

    # List all tests for a unit
    path(
        "units/<int:unit_pk>/tests/",
        views.test_list_view,
        name="test_list",
    ),

    # Create a new test
    path(
        "units/<int:unit_pk>/tests/create/",
        views.test_create_view,
        name="test_create",
    ),

    # View test details and marks
    path(
        "tests/<int:pk>/",
        views.test_detail_view,
        name="test_detail",
    ),

    # Edit a test
    path(
        "tests/<int:pk>/edit/",
        views.test_update_view,
        name="test_update",
    ),

    # Delete a test
    path(
        "tests/<int:pk>/delete/",
        views.test_delete_view,
        name="test_delete",
    ),

    # ============================================================
    # MARKS
    # ============================================================

    # Enter marks for students
    path(
        "tests/<int:pk>/marks/",
        views.marks_entry_view,
        name="marks_entry",
    ),

    # ============================================================
    # FEEDBACK
    # ============================================================

    # Give or update feedback for a result
    path(
        "results/<int:pk>/feedback/",
        views.feedback_form_view,
        name="feedback_form",
    ),

    # ============================================================
    # STUDENT RESULTS
    # ============================================================

    # Student's own results
    path(
        "my-results/",
        views.student_result_list_view,
        name="student_result_list",
    ),

    # Student's individual result
    path(
        "my-results/<int:pk>/",
        views.student_result_detail_view,
        name="student_result_detail",
    ),
]
