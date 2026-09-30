from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from core.mixins import AdminRequiredMixin
from core.views import PlaceholderView

from .forms import StudentRegistrationForm


class RegisterView(CreateView):
    """DONE (starter). Student self-registration. TODO LMS-103: tests."""

    form_class = StudentRegistrationForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("core:dashboard")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("core:dashboard")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, "Welcome! Your account has been created.")
        return response


class ProfileView(LoginRequiredMixin, TemplateView):
    """DONE (starter). Shows the logged-in user's details."""

    template_name = "accounts/profile.html"


# ---------------------------------------------------------------------------
# Everything below is a PLACEHOLDER. Replace `PlaceholderView` with the real
# generic view (ListView, CreateView, ...) and keep the access mixin!
# ---------------------------------------------------------------------------
class ProfileUpdateView(LoginRequiredMixin, PlaceholderView):
    task_id = "LMS-107"
    page_title = "Edit profile"
    hint = "Use UpdateView + a ProfileForm (limit photo to 2 MB, jpg/png)."


class UserListView(AdminRequiredMixin, PlaceholderView):
    task_id = "LMS-105"
    page_title = "Manage users"
    hint = "ListView of all users with search and role filter."


class UserCreateView(AdminRequiredMixin, PlaceholderView):
    task_id = "LMS-105"
    page_title = "Create user"
    hint = "Admin creates facilitators (and students). Profile is created by the signal."


class UserUpdateView(AdminRequiredMixin, PlaceholderView):
    task_id = "LMS-105"
    page_title = "Edit user"


class UserToggleActiveView(AdminRequiredMixin, PlaceholderView):
    task_id = "LMS-105"
    page_title = "Activate / deactivate user"
    hint = "POST only. Deactivate users, never delete them."


class FacilitatorListView(AdminRequiredMixin, PlaceholderView):
    task_id = "LMS-106"
    page_title = "Facilitators"
    hint = "List facilitators with a Grant / Revoke button for the course right."


class ToggleCourseRightView(AdminRequiredMixin, PlaceholderView):
    task_id = "LMS-106"
    page_title = "Grant / revoke course right"
    hint = "POST only. Use FacilitatorProfile.grant_course_rights(request.user) / revoke_course_rights()."
