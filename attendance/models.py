"""
attendance: class sessions and who came.

ClassSession     - one class meeting of a unit
AttendanceRecord - one student's attendance for one session
"""

from django.conf import settings
from django.db import models


class ClassSession(models.Model):
    class Mode(models.TextChoices):
        IN_PERSON = "IN_PERSON", "In person"
        ONLINE = "ONLINE", "Online"

    unit = models.ForeignKey("courses.Unit", on_delete=models.CASCADE, related_name="sessions")
    facilitator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="sessions_run")
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    topic = models.CharField(max_length=200, blank=True)
    mode = models.CharField(max_length=10, choices=Mode.choices, default=Mode.IN_PERSON)
    venue_or_link = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["-date", "-start_time"]
        constraints = [
            models.UniqueConstraint(fields=["unit", "date", "start_time"], name="unique_session_per_unit_slot"),
        ]
        indexes = [models.Index(fields=["unit", "date"])]

    def __str__(self):
        return f"{self.unit.title} on {self.date}"


class AttendanceRecord(models.Model):
    class Status(models.TextChoices):
        PRESENT = "PRESENT", "Present"
        ABSENT = "ABSENT", "Absent"
        LATE = "LATE", "Late"
        EXCUSED = "EXCUSED", "Excused"

    session = models.ForeignKey(ClassSession, on_delete=models.CASCADE, related_name="records")
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="attendance_records")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PRESENT)
    note = models.CharField(max_length=200, blank=True)
    marked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="attendance_marked",
    )
    marked_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["student__first_name", "student__last_name"]
        constraints = [
            models.UniqueConstraint(fields=["session", "student"], name="one_record_per_student_per_session"),
        ]

    def __str__(self):
        return f"{self.student} - {self.session}: {self.status}"
