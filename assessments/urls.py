from django.urls import path

from . import views

app_name = "assessments"

urlpatterns = [
    path("units/<int:unit_pk>/tests/", views.TestListView.as_view(), name="test_list"),
    path("units/<int:unit_pk>/tests/create/", views.TestCreateView.as_view(), name="test_create"),
    path("tests/<int:pk>/", views.TestDetailView.as_view(), name="test_detail"),
    path("tests/<int:pk>/edit/", views.TestUpdateView.as_view(), name="test_edit"),
    path("tests/<int:pk>/delete/", views.TestDeleteView.as_view(), name="test_delete"),
    path("tests/<int:pk>/marks/", views.MarksEntryView.as_view(), name="marks"),
    path("results/<int:pk>/feedback/", views.FeedbackFormView.as_view(), name="feedback"),
    path("my/results/", views.StudentResultListView.as_view(), name="my_results"),
    path("my/results/<int:pk>/", views.StudentResultDetailView.as_view(), name="my_result"),
]
