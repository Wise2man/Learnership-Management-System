from django.contrib import admin

from .models import Feedback, Test, TestResult


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ("title", "unit", "test_date", "total_marks", "pass_mark")
    list_filter = ("unit__course",)


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ("test", "student", "marks_obtained", "status")
    list_filter = ("status", "test")


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("result", "facilitator", "created_at")
