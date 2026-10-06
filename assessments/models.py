"""
Assessments models.

This app manages:
- Tests: assessments created inside a learning unit
- TestResults: one student's result for one test
- Feedback: facilitator feedback for a student's test result
"""

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


# ============================================================
# TEST
# ============================================================

class Test(models.Model):
    """
    Represents an assessment/test belonging to a learning unit.

    Example:
        Unit: Python Programming
        Test: Python Fundamentals Test

    A Test is created by the facilitator responsible for the unit.
    """

    

    # Prevent pytest from treating this Django model as a test class.
    __test__ = False

    # --------------------------------------------------------
    # RELATIONSHIP TO UNIT
    # --------------------------------------------------------

    # Each test belongs to one Unit.
    #
    # Example:
    # Unit 1 -> Test 1
    # Unit 1 -> Test 2
    #
    # related_name="tests" allows:
    #     unit.tests.all()
    #
    # CASCADE means that if the Unit is deleted,
    # its tests will also be deleted.
    unit = models.ForeignKey(
        "courses.Unit",
        on_delete=models.CASCADE,
        related_name="tests",
    )

    # --------------------------------------------------------
    # TEST INFORMATION
    # --------------------------------------------------------

    # Name/title of the assessment.
    title = models.CharField(max_length=200)

    # Optional description/instructions for the test.
    description = models.TextField(blank=True)

    # Maximum number of marks available for the test.
    #
    # Example:
    # total_marks = 100
    total_marks = models.PositiveSmallIntegerField(default=100)

    # Minimum mark required to pass the test.
    #
    # Example:
    # total_marks = 100
    # pass_mark = 50
    pass_mark = models.PositiveSmallIntegerField(default=50)

    # Date on which the test takes place.
    test_date = models.DateField()

    # --------------------------------------------------------
    # CREATOR
    # --------------------------------------------------------

    # The user/facilitator who created the test.
    #
    # settings.AUTH_USER_MODEL is used instead of importing
    # the User model directly. This supports custom User models.
    #
    # PROTECT prevents the creator from being deleted if
    # they still have tests associated with their account.
    #
    # related_name="tests_created" allows:
    #     user.tests_created.all()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="tests_created",
    )

    # Automatically stores when the test was created.
    created_at = models.DateTimeField(auto_now_add=True)

    # --------------------------------------------------------
    # MODEL META
    # --------------------------------------------------------

    class Meta:
        # Display the newest tests first.
        ordering = ["-test_date"]

    # --------------------------------------------------------
    # STRING REPRESENTATION
    # --------------------------------------------------------

    def __str__(self):
        """
        Controls how the Test is displayed in the Django admin
        and other places where the object is converted to text.
        """

        return f"{self.title} ({self.unit.title})"

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    def clean(self):
        """
        Validate the test before it is saved.

        The pass mark cannot be greater than the total marks.
        """

        if self.pass_mark > self.total_marks:
            raise ValidationError(
                "Pass mark cannot be more than total marks."
            )


# ============================================================
# TEST RESULT
# ============================================================

class TestResult(models.Model):
    """One student's result for a single test."""

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        MARKED = "MARKED", "Marked"
        ABSENT = "ABSENT", "Absent"

    test = models.ForeignKey(
        "Test",
        on_delete=models.CASCADE,
        related_name="results",
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="test_results",
    )
    marks_obtained = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
    )
    marked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="results_marked",
        null=True,
        blank=True,
    )
    marked_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["student__first_name", "student__last_name"]
        constraints = [
            models.UniqueConstraint(
                fields=["test", "student"],
                name="one_result_per_student_per_test",
            )
        ]

    def __str__(self):
        return f"{self.student} - {self.test} ({self.status})"


# ============================================================
# FEEDBACK
# ============================================================

class Feedback(models.Model):
    """Facilitator feedback for a student's completed test result."""

    result = models.OneToOneField(
        "TestResult",
        on_delete=models.CASCADE,
        related_name="feedback",
    )
    facilitator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="feedback_given",
    )
    comment = models.TextField()
    areas_for_improvement = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Feedback for {self.result}",