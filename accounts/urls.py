from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from . import views

app_name = "accounts"

urlpatterns = [
    path("accounts/register/", views.RegisterView, name="register"),
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(template_name="registration/login.html", redirect_authenticated_user=True),
        name="login",
    ),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path(
        "accounts/password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset.html",
            email_template_name="registration/password_reset_email.html",
            subject_template_name="registration/password_reset_subject.txt",
            success_url=reverse_lazy(
                "accounts:password_reset_done"
            ),
        ),
        name="password_reset",
    ),
    path("accounts/profile/", views.ProfileView, name="profile"),
    path("accounts/profile/edit/", views.ProfileUpdateView, name="profile_edit"),
    # Admin only
    path("manage/users/", views.UserListView, name="user_list"),
    path("manage/users/create/", views.UserCreateView, name="user_create"),
    path("manage/users/<int:pk>/edit/", views.UserUpdateView, name="user_edit"),
    path("manage/users/<int:pk>/toggle-active/", views.UserToggleActiveView, name="user_toggle"),
    path("manage/facilitators/", views.FacilitatorListView, name="fac_list"),
    path("manage/facilitators/<int:pk>/course-right/", views.ToggleCourseRightView, name="fac_right"),
]
