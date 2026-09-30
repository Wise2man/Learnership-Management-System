from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("accounts/register/", views.RegisterView.as_view(), name="register"),
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(template_name="registration/login.html", redirect_authenticated_user=True),
        name="login",
    ),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    # TODO LMS-103: password reset (4 pages): password_reset, _done, _confirm, _complete
    path("accounts/profile/", views.ProfileView.as_view(), name="profile"),
    path("accounts/profile/edit/", views.ProfileUpdateView.as_view(), name="profile_edit"),
    # Admin only
    path("manage/users/", views.UserListView.as_view(), name="user_list"),
    path("manage/users/create/", views.UserCreateView.as_view(), name="user_create"),
    path("manage/users/<int:pk>/edit/", views.UserUpdateView.as_view(), name="user_edit"),
    path("manage/users/<int:pk>/toggle-active/", views.UserToggleActiveView.as_view(), name="user_toggle"),
    path("manage/facilitators/", views.FacilitatorListView.as_view(), name="fac_list"),
    path("manage/facilitators/<int:pk>/course-right/", views.ToggleCourseRightView.as_view(), name="fac_right"),
]
