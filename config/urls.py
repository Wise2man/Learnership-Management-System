"""Root URL configuration. Each app owns its own urls.py."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("django-admin/", admin.site.urls),  # Django's built-in admin (superusers)
    path("", include("core.urls")),
    path("", include("accounts.urls")),
    path("", include("courses.urls")),
    path("", include("enrollments.urls")),
    path("", include("assessments.urls")),
    path("", include("attendance.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    try:
        import debug_toolbar

        urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
    except ImportError:
        pass
