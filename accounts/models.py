"""
accounts: who people are.

User            - one table for admin, facilitator and student (see `role`)
FacilitatorProfile - extra info + the "can manage courses" right (only Admin changes it)
StudentProfile  - extra info for students
"""

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        FACILITATOR = "FACILITATOR", "Facilitator"
        STUDENT = "STUDENT", "Student"

    email = models.EmailField("email address", unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)
    phone = models.CharField(max_length=20, blank=True)
    profile_photo = models.ImageField(upload_to="profiles/", null=True, blank=True)

    REQUIRED_FIELDS = ["email"]

    class Meta:
        ordering = ["first_name", "last_name", "username"]

    def save(self, *args, **kwargs):
        # A superuser created with `createsuperuser` is always an Admin in our app.
        if self.is_superuser:
            self.role = self.Role.ADMIN
        super().save(*args, **kwargs)

    def __str__(self):
        return self.get_full_name() or self.username

    # ---- role helpers (use these in views and templates) ----
    @property
    def is_admin_role(self):
        return self.role == self.Role.ADMIN or self.is_superuser

    @property
    def is_facilitator(self):
        return self.role == self.Role.FACILITATOR

    @property
    def is_student(self):
        return self.role == self.Role.STUDENT

    @property
    def effective_role(self):
        return self.Role.ADMIN.value if self.is_admin_role else self.role

    @property
    def can_manage_courses(self):
        """Admin: always. Facilitator: only if Admin granted the right. Student: never."""
        if self.is_admin_role:
            return True
        if not self.is_facilitator:
            return False
        profile = getattr(self, "facilitator_profile", None)
        return bool(profile and profile.can_manage_courses)


class FacilitatorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="facilitator_profile")
    bio = models.TextField(blank=True)
    qualification = models.CharField(max_length=150, blank=True)
    # THE course right. Only an Admin may change it (see grant/revoke below).
    can_manage_courses = models.BooleanField(default=False)
    granted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="course_rights_granted",
    )
    granted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Facilitator profile: {self.user}"

    def grant_course_rights(self, admin_user):
        self.can_manage_courses = True
        self.granted_by = admin_user
        self.granted_at = timezone.now()
        self.save(update_fields=["can_manage_courses", "granted_by", "granted_at"])

    def revoke_course_rights(self, admin_user):
        self.can_manage_courses = False
        self.granted_by = admin_user
        self.granted_at = timezone.now()
        self.save(update_fields=["can_manage_courses", "granted_by", "granted_at"])


class StudentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="student_profile")
    student_number = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    highest_qualification = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    emergency_contact = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.student_number} - {self.user}"
