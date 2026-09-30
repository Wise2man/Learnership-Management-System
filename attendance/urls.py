from django.urls import path

from . import views

app_name = "attendance"

urlpatterns = [
    path("units/<int:unit_pk>/sessions/", views.SessionListView.as_view(), name="session_list"),
    path("units/<int:unit_pk>/sessions/create/", views.SessionCreateView.as_view(), name="session_create"),
    path("sessions/<int:pk>/", views.SessionDetailView.as_view(), name="session_detail"),
    path("sessions/<int:pk>/mark/", views.MarkAttendanceView.as_view(), name="mark"),
    path("units/<int:unit_pk>/attendance/", views.UnitAttendanceReportView.as_view(), name="report"),
    path("units/<int:unit_pk>/attendance/export/", views.AttendanceExportView.as_view(), name="export"),
    path("my/attendance/", views.StudentAttendanceView.as_view(), name="my_attendance"),
    path("manage/attendance/", views.AdminAttendanceOverviewView.as_view(), name="overview"),
]
