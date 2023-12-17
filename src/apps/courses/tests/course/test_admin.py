from http import HTTPStatus
from pprint import pprint

from django.conf import settings
from django.contrib.admin import AdminSite
from django.contrib.auth import get_user_model

from apps.courses.admin import CourseAdmin
from apps.courses.models import Course, Subject
from utils.tests.base import AdminTestCase

User = get_user_model()


class CourseAdminTestCase(AdminTestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.site = AdminSite()
        cls.user = user = User.objects.create_superuser(  # dal later
            username=settings.DEFAULT_ADMIN_NAME,
            email=settings.DEFAULT_ADMIN_EMAIL,
            password=settings.DEFAULT_ADMIN_PASSWORD,
        )
        cls.course = Course.objects.create(  # dal layer
            title="Course1",
            owner=user,
        )
        cls.course2 = Course.objects.create(  # dal layer
            title="Course2",
            owner=user,
        )
        cls.add_change_form_required_data = {
            "modules-TOTAL_FORMS": 0,  # Number of empty and filled forms
            "modules-INITIAL_FORMS": 0,  # Number of forms with initial data
        }
        cls.site = AdminSite()

    # integration
    def test_course_is_displayed(self) -> None:
        url = self.make_url(self.site, Course, "changelist")  # DRY
        response = self.client.get(url)  # DRY
        self.assertEqual(response.status_code, HTTPStatus.OK)

    # integration
    def test_display_title_field(self) -> None:
        url = self.make_url(self.site, Course, "changelist")  # DRY
        response = self.client.get(url)  # DRY
        self.assertContains(response, "Title")

    # integration
    def test_display_slug_field(self) -> None:
        url = self.make_url(self.site, Course, "changelist")  # DRY
        response = self.client.get(url)  # DRY
        self.assertContains(response, "Slug")

    # integration
    def test_display_owner_field(self) -> None:
        url = self.make_url(self.site, Course, "changelist")  # DRY
        response = self.client.get(url)  # DRY
        self.assertContains(response, "Owner username")

    # integration
    def test_display_subject_field(self) -> None:
        url = self.make_url(self.site, Course, "changelist")  # DRY
        response = self.client.get(url)  # DRY
        self.assertContains(response, "Subject title")

    # integration
    def test_display_description_field(self) -> None:
        url = self.make_url(self.site, Course, "changelist")  # DRY
        response = self.client.get(url)  # DRY
        self.assertContains(response, "Description")

    # integration
    def test_queryset_ordering(self) -> None:
        url = self.make_url(self.site, Course, "changelist")  # DRY
        response = self.client.get(url)  # DRY
        queryset = response.context["cl"].queryset  # abstraction layer
        self.assertTrue(queryset.ordered)
        self.assertEqual([self.course2, self.course], [*queryset.all()])

    # integration
    def test_empty_subject_title(self) -> None:
        course_admin = CourseAdmin(Course, AdminSite())  # abstract layer
        empty_title = course_admin.subject_title(self.course)
        self.assertEqual(empty_title, None)

    # integration
    def test_filled_subject_title(self) -> None:
        self.course.subject = Subject.objects.create(title="Subject1")  # dal layer
        course_admin = CourseAdmin(Course, self.site)  # abstract layer
        empty_title = course_admin.subject_title(self.course)
        self.assertEqual(empty_title, "Subject1")

    # integration
    def test_short_description(self) -> None:
        module_admin = CourseAdmin(Course, self.site)  # abstract layer
        short_description = module_admin.description(self.course)
        self.assertLessEqual(len(short_description), 30)

    @staticmethod
    def _get_filtered_course_count(**kwargs) -> int:  # dal layer
        return Course.objects.filter(**kwargs).count()

    # integration
    def test_add_course(self) -> None:
        before_course_count = self._get_filtered_course_count(title="GoCourse")

        add_url = self.make_url(self.site, Course, "add")  # abstract layer
        response = self.client.post(
            add_url,
            data={
                **self.add_change_form_required_data,
                "owner": self.user.id,
                "title": "GoCourse",
                "slug": "go_course",
            },
        )
        change_list_url = self.make_url(
            self.site, Course, "changelist"
        )  # abstract layer
        self.assertRedirects(response, change_list_url)

        after_course_count = self._get_filtered_course_count(title="GoCourse")
        self.assertEqual(after_course_count, before_course_count + 1)

    # integration
    def test_change_course(self) -> None:
        before_course_count = self._get_filtered_course_count(title="GoCourse")

        change_url = self.make_url(
            self.site, Course, "change", self.course.id
        )  # abstract layer
        response = self.client.get(change_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        initial_data = response.context_data["adminform"].form.initial  # abstract layer
        filled_data = {k: v for k, v in initial_data.items() if v is not None}
        response = self.client.post(
            change_url,
            data={
                **self.add_change_form_required_data,
                **filled_data,
                "title": "GoCourse",
            },
        )
        change_list_url = self.make_url(
            AdminSite(), Course, "changelist"
        )  # abstract layer
        self.assertRedirects(response, change_list_url)

        after_course_count = self._get_filtered_course_count(title="GoCourse")
        self.assertEqual(after_course_count, before_course_count + 1)
