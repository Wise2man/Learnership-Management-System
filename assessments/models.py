""""
assessments: tests, marks and feedback.

Test       - an assessment inside a unit (created by the unit's facilitator)
TestResult - one student's mark for one test
Feedback   - the facilitator's written feedback on one result
"""

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Test(models.Model):
    __test__ = False  # Tells pytest: this is a model, not a test class

    unit = models.ForeignKey(
        "courses.Unit", on_delete=models.CASCADE, related_name="tests"
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    total_marks = models.PositiveSmallIntegerField(default=100)
    pass_mark = models.PositiveSmallIntegerField(default=50)
    test_date = models.DateField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="tests_created",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-test_date"]

    def __str__(self):
        return f"{self.title} ({self.unit.title})"

    def clean(self):
        super().clean()
        if self.pass_mark > self.total_marks:
            raise ValidationError(
                {"pass_mark": "Pass mark cannot be more than total marks."}
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class TestResult(models.Model):
    __test__ = False

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        MARKED = "MARKED", "Marked"
        ABSENT = "ABSENT", "Absent"

    test = models.ForeignKey(
        Test, on_delete=models.CASCADE, related_name="results"
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="test_results",
    )
    marks_obtained = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.PENDING
    )
    marked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="results_marked",
    )
    marked_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["student__first_name", "student__last_name"]
        constraints = [
            models.UniqueConstraint(
                fields=["test", "student"],
                name="one_result_per_student_per_test",
            ),
        ]

    def __str__(self):
        return f"{self.student} - {self.test.title}: {self.marks_obtained or 'N/A'}"

    def clean(self):
        super().clean()
        if self.status == self.Status.MARKED and self.marks_obtained is None:
            raise ValidationError(
                {"marks_obtained": "Marked status requires marks_obtained to be provided."}
            )
        if self.marks_obtained is not None:
            if self.marks_obtained > self.test.total_marks:
                raise ValidationError(
                    {"marks_obtained": "Marks cannot be more than the total marks of the test."}
                )
            if self.marks_obtained < 0:
                raise ValidationError(
                    {"marks_obtained": "Marks cannot be negative."}
                )

    def save(self, *args, **kwargs):
        # Auto-update status to MARKED if marks are added
        if self.marks_obtained is not None and self.status == self.Status.PENDING:
            self.status = self.Status.MARKED

        # Set marked_at timestamp automatically when marked
        if self.status == self.Status.MARKED and not self.marked_at:
            self.marked_at = timezone.now()

        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def passed(self):
        if self.marks_obtained is None or self.status == self.Status.ABSENT:
            return None
        return self.marks_obtained >= self.test.pass_mark

    @property
    def percentage(self):
        if self.marks_obtained is None or self.test.total_marks == 0:
            return None
        return round((self.marks_obtained / self.test.total_marks) * 100, 2)


class Feedback(models.Model):
    result = models.OneToOneField(
        TestResult, on_delete=models.CASCADE, related_name="feedback"
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