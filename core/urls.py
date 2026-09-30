from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("dashboard/", views.DashboardRedirectView.as_view(), name="dashboard"),
    path("dashboard/admin/", views.AdminDashboardView.as_view(), name="dash_admin"),
    path("dashboard/facilitator/", views.FacilitatorDashboardView.as_view(), name="dash_fac"),
    path("dashboard/student/", views.StudentDashboardView.as_view(), name="dash_student"),
]
