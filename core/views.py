from django.db.models import Q
from django.views.generic import ListView, RedirectView, TemplateView

from courses.models import Course

from .mixins import AccessControlMixin, AdminRequiredMixin, FacilitatorRequiredMixin, StudentRequiredMixin


class PlaceholderView(TemplateView):
    """
    Shows "this page is not built yet". Every unfinished page uses it so that
    ALL urls exist from day one and the menu never breaks.
    Set task_id, page_title and hint on the subclass.
    To build the page: replace PlaceholderView with a real generic view.
    """

    template_name = "placeholder.html"
    task_id = ""
    page_title = "Coming soon"
    hint = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(task_id=self.task_id, page_title=self.page_title, hint=self.hint)
        return context


class HomeView(ListView):
    """DONE (starter). Public home page: published courses with search.
    TODO LMS-207: filters (django-filter), nicer cards, empty state polish."""

    template_name = "core/home.html"
    context_object_name = "courses"
    paginate_by = 9

    def get_queryset(self):
        courses = Course.objects.on_home_page().select_related("created_by")
        q = self.request.GET.get("q", "").strip()
        if q:
            courses = courses.filter(Q(title__icontains=q) | Q(description__icontains=q))
        return courses

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = self.request.GET.get("q", "").strip()
        return context


class DashboardRedirectView(AccessControlMixin, RedirectView):
    """DONE (starter). Sends each user to the dashboard for their role."""

    def get_redirect_url(self, *args, **kwargs):
        role = self.request.user.effective_role
        return {
            "ADMIN": "/dashboard/admin/",
            "FACILITATOR": "/dashboard/facilitator/",
        }.get(role, "/dashboard/student/")


class AdminDashboardView(AdminRequiredMixin, TemplateView):
    """Placeholder dashboard. TODO LMS-601: totals, pending applications, recent activity."""

    template_name = "core/dashboard_admin.html"


class FacilitatorDashboardView(FacilitatorRequiredMixin, TemplateView):
    """Placeholder dashboard. TODO LMS-602: my units, upcoming sessions, pending feedback."""

    template_name = "core/dashboard_facilitator.html"


class StudentDashboardView(StudentRequiredMixin, TemplateView):
    """Placeholder dashboard. TODO LMS-603: courses, next sessions, latest results, attendance %."""

    template_name = "core/dashboard_student.html"
