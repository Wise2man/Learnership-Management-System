from django.urls import reverse

from accounts.models import User


def test_home_page_lists_published_course_only(client, course):
    response = client.get(reverse("core:home"))
    assert response.status_code == 200
    assert "Test Course" in response.content.decode()


def test_home_search_filters(client, course):
    assert "Test Course" not in client.get(reverse("core:home"), {"q": "nothing-like-this"}).content.decode()


def test_course_detail_is_public_for_published(client, course):
    assert client.get(course.get_absolute_url()).status_code == 200


def test_draft_course_is_hidden_from_public(client, course):
    course.status = "DRAFT"
    course.save()
    assert client.get(course.get_absolute_url()).status_code == 404


def test_register_creates_student_and_logs_in(client, db):
    response = client.post(
        reverse("accounts:register"),
        {
            "username": "newbie",
            "first_name": "New",
            "last_name": "Student",
            "email": "newbie@example.com",
            "password1": "A-strong-pass-2026",
            "password2": "A-strong-pass-2026",
        },
    )
    assert response.status_code == 302
    user = User.objects.get(username="newbie")
    assert user.role == User.Role.STUDENT
    assert user.student_profile.student_number


def test_register_rejects_duplicate_email(client, student):
    response = client.post(
        reverse("accounts:register"),
        {
            "username": "another",
            "first_name": "A",
            "last_name": "B",
            "email": student.email,
            "password1": "A-strong-pass-2026",
            "password2": "A-strong-pass-2026",
        },
    )
    assert response.status_code == 200
    assert not User.objects.filter(username="another").exists()


def test_login_and_logout(client, student):
    assert (
        client.post(reverse("accounts:login"), {"username": "student1", "password": "Password123!"}).status_code == 302
    )
    assert client.post(reverse("accounts:logout")).status_code == 302


def test_dashboard_redirects_by_role(login, admin_user, course_manager, student):
    assert login(admin_user).get(reverse("core:dashboard")).url == "/dashboard/admin/"
    assert login(course_manager).get(reverse("core:dashboard")).url == "/dashboard/facilitator/"
    assert login(student).get(reverse("core:dashboard")).url == "/dashboard/student/"


def test_every_dashboard_renders_for_its_role(login, admin_user, facilitator, student):
    assert login(admin_user).get(reverse("core:dash_admin")).status_code == 200
    assert login(facilitator).get(reverse("core:dash_fac")).status_code == 200
    assert login(student).get(reverse("core:dash_student")).status_code == 200
