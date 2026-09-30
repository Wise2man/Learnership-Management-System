from django.urls import path

from . import views

app_name = "courses"

# IMPORTANT: fixed words ("manage/", "create/") must come BEFORE <slug:slug>/
urlpatterns = [
    path("courses/manage/", views.ManageCourseListView.as_view(), name="manage"),
    path("courses/create/", views.CourseCreateView.as_view(), name="create"),
    path("teaching/units/", views.MyUnitsView.as_view(), name="my_units"),
    path("courses/<slug:slug>/", views.CourseDetailView.as_view(), name="detail"),
    path("courses/<slug:slug>/edit/", views.CourseUpdateView.as_view(), name="edit"),
    path("courses/<slug:slug>/delete/", views.CourseDeleteView.as_view(), name="delete"),
    path("courses/<slug:slug>/status/", views.CourseStatusView.as_view(), name="status"),
    path("courses/<slug:slug>/units/", views.UnitListView.as_view(), name="unit_list"),
    path("courses/<slug:slug>/units/add/", views.UnitCreateView.as_view(), name="unit_add"),
    path("courses/<slug:slug>/units/<int:pk>/edit/", views.UnitUpdateView.as_view(), name="unit_edit"),
    path("courses/<slug:slug>/units/<int:pk>/delete/", views.UnitDeleteView.as_view(), name="unit_delete"),
]
