"""
Business rules for applying and enrolling. Write these as plain functions, then call them from views.

TODO LMS-303  apply_for_course(student, course, motivation)
              rules: course open for applications, not full, student has not applied before
TODO LMS-306  approve_application(application, reviewer, note="")
              rules: wrap in transaction.atomic(); re-check capacity; create the Enrollment
              reject_application(application, reviewer, note)
"""
