from django.contrib import admin

from .models import Application, Enrollment


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "status", "applied_at", "reviewed_by")
    list_filter = ("status", "course")


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "status", "enrolled_at")
    list_filter = ("status", "course")
