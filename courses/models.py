"""
courses: what students apply for.

Course - created by an Admin or a facilitator who has the course right
Unit   - a module inside a course, taught by ONE facilitator
"""

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


class CourseQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status=Course.Status.PUBLISHED)

    def on_home_page(self):
        """Published courses whose application window has not ended yet."""
        return self.published().filter(application_close__gte=timezone.localdate())


class Course(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        PUBLISHED = "PUBLISHED", "Published"
        CLOSED = "CLOSED", "Closed"
        ARCHIVED = "ARCHIVED", "Archived"

    # These words are URLs of their own (/courses/create/), so no course may use them as slug.
    RESERVED_SLUGS = {"create", "manage"}

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to="courses/", null=True, blank=True)
    duration_weeks = models.PositiveSmallIntegerField(default=12)
    capacity = models.PositiveIntegerField(null=True, blank=True, help_text="Leave empty for unlimited")
    application_open = models.DateField()
    application_close = models.DateField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="courses_created")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CourseQuerySet.as_manager()

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["status", "application_close"])]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._make_unique_slug()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("courses:detail", kwargs={"slug": self.slug})

    def _make_unique_slug(self):
        base = slugify(self.title) or "course"
        slug, n = base, 2
        while slug in self.RESERVED_SLUGS or Course.objects.filter(slug=slug).exists():
            slug = f"{base}-{n}"
            n += 1
        return slug

    @property
    def is_published(self):
        return self.status == self.Status.PUBLISHED

    @property
    def is_open_for_applications(self):
        today = timezone.localdate()
        return self.is_published and self.application_open <= today <= self.application_close

    @property
    def enrolled_count(self):
        return self.enrollments.filter(status="ACTIVE").count()

    @property
    def seats_left(self):
        if self.capacity is None:
            return None
        return max(self.capacity - self.enrolled_count, 0)

    @property
    def is_full(self):
        return self.capacity is not None and self.enrolled_count >= self.capacity


class Unit(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="units")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveSmallIntegerField(default=1)
    hours = models.PositiveSmallIntegerField(null=True, blank=True, help_text="Notional learning hours")
    facilitator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="units_taught",
        limit_choices_to={"role": "FACILITATOR"},
    )

    class Meta:
        ordering = ["course", "order"]
        constraints = [
            models.UniqueConstraint(fields=["course", "order"], name="unique_unit_order_per_course"),
        ]

    def __str__(self):
        return f"{self.course.title} / {self.order}. {self.title}"
