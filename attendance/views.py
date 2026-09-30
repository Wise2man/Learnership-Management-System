from django.shortcuts import get_object_or_404

from core.mixins import AdminRequiredMixin, StudentRequiredMixin, UnitFacilitatorRequiredMixin
from core.views import PlaceholderView

from .models import ClassSession


class SessionUnitMixin(UnitFacilitatorRequiredMixin):
    """For URLs like /sessions/<pk>/ : the unit comes from the ClassSession."""

    def get_unit(self):
        return get_object_or_404(ClassSession, pk=self.kwargs["pk"]).unit


class SessionListView(UnitFacilitatorRequiredMixin, PlaceholderView):
    task_id = "LMS-502"
    page_title = "Class sessions"


class SessionCreateView(UnitFacilitatorRequiredMixin, PlaceholderView):
    task_id = "LMS-502"
    page_title = "Create class session"
    hint = "Set unit = self.unit and facilitator = request.user."


class SessionDetailView(SessionUnitMixin, PlaceholderView):
    task_id = "LMS-502"
    page_title = "Session details"


class MarkAttendanceView(SessionUnitMixin, PlaceholderView):
    task_id = "LMS-503"
    page_title = "Mark attendance"
    hint = "Formset: one row per ACTIVE student, default PRESENT. Add a 'mark all present' button."


class UnitAttendanceReportView(UnitFacilitatorRequiredMixin, PlaceholderView):
    task_id = "LMS-504"
    page_title = "Attendance report"
    hint = "Attendance % per student. Highlight below settings.LOW_ATTENDANCE_THRESHOLD."


class AttendanceExportView(UnitFacilitatorRequiredMixin, PlaceholderView):
    task_id = "LMS-505"
    page_title = "Export attendance"
    hint = "CSV first (csv module), PDF second (reportlab is installed)."


class StudentAttendanceView(StudentRequiredMixin, PlaceholderView):
    task_id = "LMS-506"
    page_title = "My attendance"
    hint = "Use attendance.selectors.records_for_student(request.user)."


class AdminAttendanceOverviewView(AdminRequiredMixin, PlaceholderView):
    task_id = "LMS-507"
    page_title = "Attendance overview"
