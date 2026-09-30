"""
Access-control mixins. Put the mixin FIRST in the class bases:

    class CourseCreateView(CourseManagerRequiredMixin, CreateView): ...

Rules (see the plan, section 2):
    RoleRequiredMixin            user.role must be in `allowed_roles`
    AdminRequiredMixin           Admin only
    StudentRequiredMixin         Student only
    FacilitatorRequiredMixin     Facilitator or Admin
    CourseManagerRequiredMixin   Admin, or facilitator with the course right
    CourseOwnerMixin             ... AND owns the course in URL kwarg `slug` (admin: any)
    UnitFacilitatorRequiredMixin Admin, or the facilitator of the unit (`get_unit()`)

Anonymous users are redirected to login. Wrong role -> 403 page.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from . import permissions


class AccessControlMixin(LoginRequiredMixin):
    """Base class. Subclasses override `check_access` and raise PermissionDenied."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        self.check_access(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)

    def check_access(self, request, *args, **kwargs):
        """Raise PermissionDenied if the user may not continue."""


class RoleRequiredMixin(AccessControlMixin):
    allowed_roles = ()  # e.g. ("ADMIN", "FACILITATOR")

    def check_access(self, request, *args, **kwargs):
        super().check_access(request, *args, **kwargs)
        if request.user.effective_role not in self.allowed_roles:
            raise PermissionDenied


class AdminRequiredMixin(RoleRequiredMixin):
    allowed_roles = ("ADMIN",)


class StudentRequiredMixin(RoleRequiredMixin):
    allowed_roles = ("STUDENT",)


class FacilitatorRequiredMixin(RoleRequiredMixin):
    allowed_roles = ("ADMIN", "FACILITATOR")


class CourseManagerRequiredMixin(AccessControlMixin):
    def check_access(self, request, *args, **kwargs):
        super().check_access(request, *args, **kwargs)
        if not permissions.can_manage_courses(request.user):
            raise PermissionDenied


class CourseOwnerMixin(CourseManagerRequiredMixin):
    """Loads the course from the `slug` URL kwarg and checks ownership. Sets self.course."""

    def check_access(self, request, *args, **kwargs):
        super().check_access(request, *args, **kwargs)
        from courses.models import Course

        course = get_object_or_404(Course, slug=kwargs["slug"])
        if not permissions.can_edit_course(request.user, course):
            raise PermissionDenied
        self.course = course


class UnitFacilitatorRequiredMixin(AccessControlMixin):
    """
    Admin, or the facilitator who teaches the unit. Sets self.unit (may be None
    for pages that are not tied to one unit).
    Override get_unit() when the URL has no `unit_pk` (e.g. /tests/<pk>/).
    """

    unit = None

    def get_unit(self):
        from courses.models import Unit

        unit_pk = self.kwargs.get("unit_pk")
        return get_object_or_404(Unit, pk=unit_pk) if unit_pk else None

    def check_access(self, request, *args, **kwargs):
        super().check_access(request, *args, **kwargs)
        self.kwargs = kwargs
        if request.user.effective_role not in ("ADMIN", "FACILITATOR"):
            raise PermissionDenied
        self.unit = self.get_unit()
        if self.unit is not None and not permissions.can_teach_unit(request.user, self.unit):
            raise PermissionDenied
