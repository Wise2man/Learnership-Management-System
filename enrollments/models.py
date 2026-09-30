"""
enrollments: applying for a course and being accepted.

Application - a student asks to join a course (PENDING -> APPROVED / REJECTED / WITHDRAWN)
Enrollment  - created when an application is APPROVED (see services.approve_application, LMS-306)
"""

from django.conf import settings
from django.db import models


class Application(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"
        WITHDRAWN = "WITHDRAWN", "Withdrawn"

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applications")
    course = models.ForeignKey("courses.Course", on_delete=models.CASCADE, related_name="applications")
    motivation = models.TextField(help_text="Why do you want this course?")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    applied_at = models.DateTimeField(auto_now_add=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="applications_reviewed",
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    review_note = models.TextField(blank=True)

    class Meta:
        ordering = ["-applied_at"]
        constraints = [
            models.UniqueConstraint(fields=["student", "course"], name="one_application_per_student_per_course"),
        ]
        indexes = [models.Index(fields=["status"])]

    def __str__(self):
        return f"{self.student} -> {self.course} ({self.status})"


class Enrollment(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        COMPLETED = "COMPLETED", "Completed"
        DROPPED = "DROPPED", "Dropped"

    application = models.OneToOneField(Application, on_delete=models.PROTECT, related_name="enrollment")
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey("courses.Course", on_delete=models.CASCADE, related_name="enrollments")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-enrolled_at"]
        constraints = [
            models.UniqueConstraint(fields=["student", "course"], name="one_enrollment_per_student_per_course"),
        ]

    def __str__(self):
        return f"{self.student} in {self.course} ({self.status})"
