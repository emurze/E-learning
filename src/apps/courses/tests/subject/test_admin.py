from unittest import skip

from django.urls import reverse

from apps.courses.admin import SubjectAdmin
from apps.courses.models import Subject
from utils.tests.base import AdminTestCase


class SubjectAdminTestCase(AdminTestCase):
    model_name: str = "subject"

    @skip
    def test_subject_is_displayed(self) -> None:
        url = reverse("admin:courses_subject_changelist")
        request = self.request_factory.get(url)
        request.user = self.user

        response = SubjectAdmin(Subject, self.user).changelist_view(request)

        self.assertContains(response, "Subject1")
