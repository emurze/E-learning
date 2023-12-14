from http import HTTPStatus

from django.contrib.admin import AdminSite

from apps.courses.models import Subject
from utils.tests.base import AdminTestCase


class SubjectAdminTestCase(AdminTestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.subject = Subject.objects.create(title="Subject1")
        cls.subject2 = Subject.objects.create(title="Subject2")

    # integration
    def test_subject_is_displayed(self) -> None:
        url = self.make_url(AdminSite(), Subject, "changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    # integration
    def test_display_field_title(self) -> None:
        url = self.make_url(AdminSite(), Subject, "changelist")
        response = self.client.get(url)
        self.assertContains(response, "Title")

    # integration
    def test_display_field_slug(self) -> None:
        url = self.make_url(AdminSite(), Subject, "changelist")
        response = self.client.get(url)
        self.assertContains(response, "slug")

    # integration
    def test_ordering_by_title(self) -> None:
        url = self.make_url(AdminSite(), Subject, "changelist")
        response = self.client.get(url)
        queryset = response.context['cl'].queryset

        self.assertTrue(queryset.ordered)
        self.assertEqual(
            [self.subject, self.subject2],
            [*queryset.all()],
        )
