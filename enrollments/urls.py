from django.urls import path

from . import views

app_name = "enrollments"

urlpatterns = [
    path("courses/<slug:slug>/apply/", views.ApplyView.as_view(), name="apply"),
    path("applications/mine/", views.MyApplicationsView.as_view(), name="my_apps"),
    path("applications/<int:pk>/withdraw/", views.WithdrawView.as_view(), name="withdraw"),
    path("manage/applications/", views.ApplicationListView.as_view(), name="app_list"),
    path("manage/applications/<int:pk>/", views.ApplicationDetailView.as_view(), name="app_detail"),
    path("manage/applications/<int:pk>/approve/", views.ApproveView.as_view(), name="approve"),
    path("manage/applications/<int:pk>/reject/", views.RejectView.as_view(), name="reject"),
    path("my/courses/", views.MyEnrollmentsView.as_view(), name="my_courses"),
    path("units/<int:unit_pk>/students/", views.UnitRosterView.as_view(), name="roster"),
]
