from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    AdminUserForm,
    ProfileForm,
    StudentRegistrationForm,
)
from .models import User

def RegisterView(request):
    if request.user.is_authenticated:
        return redirect("core:dashbord")
    
    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            
            messages.success(
                request,
                "Your account was successfully created."
            )
            
            return redirect("core:dashboard")
        
    else:
        form = StudentRegistrationForm()
        return render(
            request,
            "accounts/register.html",
            {"form": form}
        )

@login_required        
def ProfileUpdateView(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Your profile was successfully updated."
            )
            return redirect("accounts:profile")
    else:
        form = ProfileForm(instance=request.user)
    
    return render(
        request,
        "accounts/profile_edit.html",
        {"form": form}
    )
    
@login_required
def ProfileView(request):
    return render(
        request,
        "accounts/profile.html"
    )
    
def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_admin:
            messages.error(request, "You do not have permission to access this page.")
            return redirect("accounts:login")
        return view_func(request, *args, **kwargs)
    return wrapper

@admin_required
def UserCreateView(request):
    if request.method == "POST":
        form = AdminUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            messages.success(
                request,
                "User was successfully created."
            )
            return redirect("accounts:user_list")
    else:
        form = AdminUserForm()
    
    return render(
        request,
        "accounts/user_form.html",
        {"form": form}
    )
    
@admin_required
def UserListView(request):
    users = User.objects.all()
    return render(
        request,
        "accounts/user_list.html",
        {"users": users}
    )
    
@admin_required
def FacilitatorListView(request):
    facilitators = User.objects.filter(role=User.Role.FACILITATOR).select_related("facilitator_profile")
    return render(
        request,
        "accounts/facilitator_list.html",
        {"facilitators": facilitators}
    )

@admin_required
def UserUpdateView(request, pk):
    user = get_object_or_404(User, pk=pk)
    
    if request.method == "POST":
        form = AdminUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "User was successfully updated."
            )
            return redirect("accounts:user_list")
    else:
        form = AdminUserForm(instance=user)
    
    return render(
        request,
        "accounts/user_form.html",
        {"form": form}
    )
    
@admin_required
def UserToggleActiveView(request, pk):
    if request.method != "POST":
        return redirect("accounts:user_list")
    
    user = get_object_or_404(User, pk=pk)
    if user == request.user:
        messages.error(
            request,
            "You cannot deactivate your own account."
        )
        return redirect("accounts:user_list")
    
    user.is_active = not user.is_active
    user.save(update_fields=["is_active"])

    status = "activated" if user.is_active else "deactivated"
    messages.success(
        request,
        f"User was successfully {status}."
    )

    return redirect("accounts:user_list")

@admin_required
def ToggleCourseRightView(request, pk):
    if request.method != "POST":
        return redirect("accounts:fac_list")
    
    facilitator = get_object_or_404(
        User,
        pk=pk,
        role=User.Role.FACILITATOR
    )
    
    profile = getattr(facilitator, "facilitator_profile", None)
    if profile is None:
        messages.error(
            request,
            "Facilitator profile not found."
        )
        return redirect("accounts:fac_list")
    if profile.can_manage_courses:
        profile.revoke_course_rights(request.user)
        messages.success(
            request,
            f"Course management rights revoked for {facilitator.get_full_name()}."
        )
        
    else:
        profile.grant_course_rights(request.user)
        messages.success(
            request,
            f"Course management rights granted to {facilitator.get_full_name()}."
        )
        
    return redirect("accounts:fac_list")