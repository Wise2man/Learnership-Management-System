from core.mixins import CourseManagerRequiredMixin, StudentRequiredMixin, UnitFacilitatorRequiredMixin
from core.views import PlaceholderView


class ApplyView(StudentRequiredMixin, PlaceholderView):
    task_id = "LMS-303"
    page_title = "Apply for course"
    hint = "URL has <slug>. Use enrollments.services.apply_for_course()."


class MyApplicationsView(StudentRequiredMixin, PlaceholderView):
    task_id = "LMS-304"
    page_title = "My applications"


class WithdrawView(StudentRequiredMixin, PlaceholderView):
    task_id = "LMS-304"
    page_title = "Withdraw application"
    hint = "POST only. Object-level check: application.student == request.user."


class ApplicationListView(CourseManagerRequiredMixin, PlaceholderView):
    task_id = "LMS-305"
    page_title = "Applications to review"
    hint = "Use enrollments.selectors.applications_for_reviewer(). Filter by status and course."


class ApplicationDetailView(CourseManagerRequiredMixin, PlaceholderView):
    task_id = "LMS-305"
    page_title = "Application details"
    hint = "Object-level check: core.permissions.can_review_applications(user, application.course)."


class ApproveView(CourseManagerRequiredMixin, PlaceholderView):
    task_id = "LMS-306"
    page_title = "Approve application"
    hint = "POST only. Call enrollments.services.approve_application()."


class RejectView(CourseManagerRequiredMixin, PlaceholderView):
    task_id = "LMS-306"
    page_title = "Reject application"
    hint = "POST only. A note is required."


class MyEnrollmentsView(StudentRequiredMixin, PlaceholderView):
    task_id = "LMS-308"
    page_title = "My courses"


class UnitRosterView(UnitFacilitatorRequiredMixin, PlaceholderView):
    task_id = "LMS-308"
    page_title = "Students in this unit"
    hint = "Use enrollments.selectors.active_students_for_unit(self.unit)."
