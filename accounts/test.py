from django.test import TestCase
from django.urls import reverse

from .models import User


class StudentRegistrationTest(TestCase):

    def test_student_can_register(self):
        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "student1",
                "first_name": "John",
                "last_name": "Doe",
                "email": "john@example.com",
                "password1": "StrongPassword123!",
                "password2": "StrongPassword123!",
            },
        )

        print("STATUS:", response.status_code)
        print("LOCATION:", response.get("Location"))

        user = User.objects.get(username="student1")

        print("USER:", user)
        print("ROLE:", user.role)

        print(
            "AUTHENTICATED:",
            "_auth_user_id" in self.client.session,
        )

        self.assertEqual(
            user.role,
            User.Role.STUDENT,
        )
