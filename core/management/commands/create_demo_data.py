"""
python manage.py create_demo_data

Creates fake users, courses, applications, a test and an attendance session so every
developer has data to work with. Safe to run many times. DEV ONLY (refuses to run if DEBUG=False).

Logins (password for all: Password123!):
    admin1                      Admin
    fac_manager (has the course right)   fac_plain (no course right)
    student1 ... student5
"""

from datetime import date, time, timedelta

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from accounts.models import User
from assessments.models import Feedback, Test, TestResult
from attendance.models import AttendanceRecord, ClassSession
from courses.models import Course, Unit
from enrollments.models import Application, Enrollment

PASSWORD = "Password123!"


class Command(BaseCommand):
    help = "Create demo data for development."

    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise CommandError("create_demo_data only runs when DEBUG=True.")

        admin, _ = User.objects.get_or_create(
            username="admin1",
            defaults=dict(
                email="admin1@example.com",
                first_name="Ada",
                last_name="Admin",
                role="ADMIN",
                is_superuser=True,
                is_staff=True,
            ),
        )
        admin.set_password(PASSWORD)
        admin.save()

        def make(username, first, last, role):
            user, _ = User.objects.get_or_create(
                username=username,
                defaults=dict(email=f"{username}@example.com", first_name=first, last_name=last, role=role),
            )
            user.set_password(PASSWORD)
            user.save()
            return user

        manager = make("fac_manager", "Thabo", "Mokoena", "FACILITATOR")
        manager.facilitator_profile.grant_course_rights(admin)
        plain = make("fac_plain", "Lerato", "Nkosi", "FACILITATOR")
        students = [
            make(f"student{i}", name, "Student", "STUDENT")
            for i, name in enumerate(["Sipho", "Nomsa", "Tebogo", "Khanyi", "Musa"], start=1)
        ]

        today = timezone.localdate()
        published, _ = Course.objects.get_or_create(
            title="Business Administration Learnership",
            defaults=dict(
                description="A 12 month learnership combining classroom learning and workplace practice.",
                duration_weeks=52,
                capacity=30,
                status="PUBLISHED",
                created_by=manager,
                application_open=today - timedelta(days=7),
                application_close=today + timedelta(days=30),
                start_date=today + timedelta(days=45),
                end_date=today + timedelta(days=45 + 365),
            ),
        )
        Course.objects.get_or_create(
            title="Software Development Learnership (draft)",
            defaults=dict(
                description="Draft course - not visible on the home page yet.",
                status="DRAFT",
                created_by=manager,
                application_open=today,
                application_close=today + timedelta(days=60),
                start_date=today + timedelta(days=90),
                end_date=today + timedelta(days=90 + 365),
            ),
        )
        unit1, _ = Unit.objects.get_or_create(
            course=published, order=1, defaults=dict(title="Workplace Communication", facilitator=manager, hours=40)
        )
        Unit.objects.get_or_create(
            course=published, order=2, defaults=dict(title="Office Administration", facilitator=plain, hours=60)
        )

        for i, student in enumerate(students):
            status = "APPROVED" if i < 3 else "PENDING"
            app, _ = Application.objects.get_or_create(
                student=student,
                course=published,
                defaults=dict(
                    motivation="I want to grow my career and gain practical experience.",
                    status=status,
                    reviewed_by=admin if status == "APPROVED" else None,
                    reviewed_at=timezone.now() if status == "APPROVED" else None,
                ),
            )
            if status == "APPROVED":
                Enrollment.objects.get_or_create(application=app, defaults=dict(student=student, course=published))

        test, _ = Test.objects.get_or_create(
            unit=unit1, title="Communication Test 1", defaults=dict(test_date=date.today(), created_by=manager)
        )
        session, _ = ClassSession.objects.get_or_create(
            unit=unit1,
            date=today,
            start_time=time(9, 0),
            defaults=dict(end_time=time(11, 0), facilitator=manager, topic="Introduction"),
        )
        for i, student in enumerate(students[:3]):
            result, _ = TestResult.objects.get_or_create(
                test=test,
                student=student,
                defaults=dict(marks_obtained=45 + i * 20, status="MARKED", marked_by=manager, marked_at=timezone.now()),
            )
            if i == 0:
                Feedback.objects.get_or_create(
                    result=result, defaults=dict(facilitator=manager, comment="Good effort. Work on structure.")
                )
            AttendanceRecord.objects.get_or_create(
                session=session,
                student=student,
                defaults=dict(status="PRESENT" if i != 2 else "ABSENT", marked_by=manager),
            )

        self.stdout.write(self.style.SUCCESS("Demo data ready. Password for every user: %s" % PASSWORD))
        self.stdout.write("Log in as: admin1, fac_manager, fac_plain, student1..student5")
