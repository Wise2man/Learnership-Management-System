from django.contrib import admin

from .models import AttendanceRecord, ClassSession


class RecordInline(admin.TabularInline):
    model = AttendanceRecord
    extra = 0


@admin.register(ClassSession)
class ClassSessionAdmin(admin.ModelAdmin):
    list_display = ("unit", "date", "start_time", "facilitator", "mode")
    list_filter = ("unit__course", "mode")
    inlines = [RecordInline]


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ("session", "student", "status")
    list_filter = ("status",)
