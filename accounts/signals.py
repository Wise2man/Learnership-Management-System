from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import FacilitatorProfile, StudentProfile, User


@receiver(post_save, sender=User)
def create_profile_for_role(sender, instance, **kwargs):
    """Every facilitator/student automatically gets the matching profile."""
    if instance.role == User.Role.FACILITATOR:
        FacilitatorProfile.objects.get_or_create(user=instance)
    elif instance.role == User.Role.STUDENT:
        StudentProfile.objects.get_or_create(
            user=instance,
            defaults={"student_number": f"STU-{timezone.now().year}-{instance.pk:04d}"},
        )
