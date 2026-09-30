from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import FacilitatorProfile, StudentProfile, User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "role", "is_active")
    list_filter = ("role", "is_active")
    fieldsets = DjangoUserAdmin.fieldsets + (("LMS", {"fields": ("role", "phone", "profile_photo")}),)
    add_fieldsets = DjangoUserAdmin.add_fieldsets + (("LMS", {"fields": ("email", "role")}),)


@admin.register(FacilitatorProfile)
class FacilitatorProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "can_manage_courses", "granted_by", "granted_at")
    list_filter = ("can_manage_courses",)


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("student_number", "user", "highest_qualification")
    search_fields = ("student_number", "user__username", "user__email")
