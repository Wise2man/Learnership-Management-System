from django.contrib import admin

from .models import Course, Unit


class UnitInline(admin.TabularInline):
    model = Unit
    extra = 0


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "application_close", "start_date", "created_by")
    list_filter = ("status",)
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [UnitInline]


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "order", "facilitator")
    list_filter = ("course",)
