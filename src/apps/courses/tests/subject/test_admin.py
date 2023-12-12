from http import HTTPStatus

from django.contrib.admin import AdminSite

from apps.courses.models import Subject
from utils.tests.base import AdminTestCase


class SubjectAdminTestCase(AdminTestCase):
    """Task: Write unittests"""

    def setUp(self) -> None:
        super().setUp()
        self.subject = Subject.objects.create(title='__SUBJECT__')

    # integration
    def test_subject_is_displayed(self) -> None:
        url = self.make_url(AdminSite(), Subject, "changelist")
        response = self.client.get(url)
        assert response.status_code == HTTPStatus.OK

    # integration
    def test_show_subject_instance(self) -> None:
        url = self.make_url(AdminSite(), Subject, "changelist")
        response = self.client.get(url)
        self.assertContains(response, '__SUBJECT__')

    # integration
    def test_show_title_field(self) -> None:
        url = self.make_url(AdminSite(), Subject, "changelist")
        response = self.client.get(url)
        self.assertContains(response, 'Title')
