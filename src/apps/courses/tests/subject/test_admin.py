from http import HTTPStatus
from pprint import pprint

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
        url = self.make_url(self.site, Subject, "changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    # integration
    def test_display_field_title(self) -> None:
        url = self.make_url(self.site, Subject, "changelist")
        response = self.client.get(url)
        self.assertContains(response, "Title")

    # integration
    def test_display_field_slug(self) -> None:
        url = self.make_url(self.site, Subject, "changelist")
        response = self.client.get(url)
        self.assertContains(response, "slug")

    # integration
    def test_ordering_by_title(self) -> None:
        url = self.make_url(self.site, Subject, "changelist")
        response = self.client.get(url)
        queryset = self.get_queryset(response)

        self.assertTrue(queryset.ordered)
        self.assertEqual(
            [self.subject, self.subject2],
            [*queryset.all()],
        )

    @staticmethod
    def _get_filtered_subject_count(**kwargs) -> int:
        return Subject.objects.filter(**kwargs).count()

    # integration
    def test_add_subject(self) -> None:
        before_course_count = self._get_filtered_subject_count(title="CCourse")

        add_url = self.make_url(self.site, Subject, "add")
        response = self.client.post(
            add_url,
            data={"title": "CCourse", "slug": "c_course"},
        )
        change_list_url = self.make_url(self.site, Subject, "changelist")
        self.assertRedirects(response, change_list_url)

        after_course_count = self._get_filtered_subject_count(title="CCourse")
        self.assertEqual(after_course_count, before_course_count + 1)

    # integration
    def test_change_subject(self) -> None:
        before_subject_count = self._get_filtered_subject_count(title="Course")

        subject_id = self.subject.id
        change_url = self.make_url(
            self.site, Subject, "change", subject_id
        )  # abstract layer
        response = self.client.get(change_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        initial_data = response.context_data["adminform"].form.initial  # abstract layer
        filled_data = {k: v for k, v in initial_data.items() if v is not None}
        response = self.client.post(
            change_url,
            data={
                **filled_data,
                "title": "Course",
            },
        )
        change_list_url = self.make_url(
            self.site, Subject, "changelist"
        )  # abstract layer
        self.assertRedirects(response, change_list_url)

        after_subject_count = self._get_filtered_subject_count(title="Course")
        self.assertEqual(after_subject_count, before_subject_count + 1)
