from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class StudentRegistrationForm(UserCreationForm):
    """Public sign-up. The role is ALWAYS forced to STUDENT."""

    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email")

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.STUDENT
        if commit:
            user.save()
        return user

class FacilitatorRegistrationForm(UserCreationForm):
    
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email")
    
    def clean_email(self):
        email = self.cleaned_data["email".lower]
        if User.objects.filter(email__iexact =email).exists():
            raise forms.ValidationError("Facilitator with thatv email exists")
        return email
    
    def save(self, commit = True):
        user = super().save(commit = False)
        user.role = User.Role.FACILITATOR
        if commit:
            user.save
        return user
    
# TODO LMS-105: AdminUserForm (admin creates facilitators / edits users)
# TODO LMS-107: ProfileForm (photo size and type limits)
