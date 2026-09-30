from django.db.models import Q
from django.views.generic import DetailView

from core.mixins import (
    CourseManagerRequiredMixin,
    CourseOwnerMixin,
    FacilitatorRequiredMixin,
)
from core.views import PlaceholderView

from .models import Course


class CourseDetailView(DetailView):
    """DONE (starter). Public course page. TODO LMS-208: polish + Apply button states."""

    model = Course
    template_name = "courses/course_detail.html"
    context_object_name = "course"

    def get_queryset(self):
        user = self.request.user
        courses = Course.objects.select_related("created_by").prefetch_related("units__facilitator")
        visible = Q(status__in=[Course.Status.PUBLISHED, Course.Status.CLOSED])
        if user.is_authenticated:
            if user.is_admin_role:
                return courses
            if user.can_manage_courses:
                visible |= Q(created_by=user)  # a manager can preview their own drafts
        return courses.filter(visible)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user, course = self.request.user, self.object
        application = None
        if user.is_authenticated and user.is_student:
            application = user.applications.filter(course=course).first()
        context["application"] = application
        context["can_apply"] = (
            user.is_authenticated
            and user.is_student
            and application is None
            and course.is_open_for_applications
            and not course.is_full
        )
        return context


# ---------------------------------------------------------------------------
# PLACEHOLDERS - replace PlaceholderView with the real generic view; KEEP the mixin.
# ---------------------------------------------------------------------------
class ManageCourseListView(CourseManagerRequiredMixin, PlaceholderView):
    task_id = "LMS-209"
    page_title = "Manage courses"
    hint = "Table of courses (use courses.selectors.courses_for_manager). Status badges, edit/delete/publish buttons."


class CourseCreateView(CourseManagerRequiredMixin, PlaceholderView):
    task_id = "LMS-203"
    page_title = "Create course"
    hint = "CreateView + CourseForm (LMS-204). Set created_by = request.user in form_valid()."


class CourseUpdateView(CourseOwnerMixin, PlaceholderView):
    task_id = "LMS-203"
    page_title = "Edit course"


class CourseDeleteView(CourseOwnerMixin, PlaceholderView):
    task_id = "LMS-203"
    page_title = "Delete course"
    hint = "Block deleting a course that has enrollments - archive it instead."


class CourseStatusView(CourseOwnerMixin, PlaceholderView):
    task_id = "LMS-205"
    page_title = "Publish / close course"
    hint = "POST only. Change status DRAFT -> PUBLISHED -> CLOSED."


class UnitListView(CourseOwnerMixin, PlaceholderView):
    task_id = "LMS-206"
    page_title = "Course units"


class UnitCreateView(CourseOwnerMixin, PlaceholderView):
    task_id = "LMS-206"
    page_title = "Add unit"
    hint = "Assign a facilitator. Order must be unique in the course."


class UnitUpdateView(CourseOwnerMixin, PlaceholderView):
    task_id = "LMS-206"
    page_title = "Edit unit"


class UnitDeleteView(CourseOwnerMixin, PlaceholderView):
    task_id = "LMS-206"
    page_title = "Delete unit"


class MyUnitsView(FacilitatorRequiredMixin, PlaceholderView):
    task_id = "LMS-210"
    page_title = "My units"
    hint = "Use courses.selectors.units_for_facilitator(request.user)."
