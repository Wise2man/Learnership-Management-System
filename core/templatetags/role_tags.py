from django import template

register = template.Library()


@register.filter
def has_role(user, role):
    """Usage: {% if request.user|has_role:'ADMIN' %} ... {% endif %}"""
    return user.is_authenticated and user.effective_role == role


@register.filter
def badge_class(status):
    """Bootstrap colour for a status word. Usage: class="badge {{ s|badge_class }}" """
    good = {"APPROVED", "PRESENT", "PASSED", "ACTIVE", "COMPLETED", "PUBLISHED", "MARKED"}
    warn = {"PENDING", "LATE", "DRAFT", "EXCUSED", "CLOSED"}
    bad = {"REJECTED", "ABSENT", "FAILED", "DROPPED", "WITHDRAWN", "ARCHIVED"}
    s = str(status).upper()
    if s in good:
        return "text-bg-success"
    if s in warn:
        return "text-bg-warning"
    if s in bad:
        return "text-bg-danger"
    return "text-bg-secondary"
