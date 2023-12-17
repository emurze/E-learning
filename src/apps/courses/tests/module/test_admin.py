from http import HTTPStatus

from django.conf import settings
from django.contrib.admin import AdminSite
from django.contrib.auth import get_user_model

from apps.courses.admin import ModuleAdmin
from apps.courses.models import Module, Course
from utils.tests.base import AdminTestCase

User = get_user_model()


class ModuleAdminTestCase(AdminTestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.site = AdminSite()
        cls.user = user = User.objects.create_superuser(
            username=settings.DEFAULT_ADMIN_NAME,
            email=settings.DEFAULT_ADMIN_EMAIL,
            password=settings.DEFAULT_ADMIN_PASSWORD,
        )
        cls.course = course = Course.objects.create(
            title="Course1",
            owner=user,
        )
        cls.module = Module.objects.create(
            title="Module1",
            course=course,
            description="Best description" * 10,
        )
        cls.module2 = Module.objects.create(
            title="Module2",
            course=course,
            description="Best description" * 10,
        )

    # integration
    def test_module_is_displayed(self) -> None:
        url = self.make_url(AdminSite(), Module, "changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    # integration
    def test_display_field_title(self) -> None:
        url = self.make_url(AdminSite(), Module, "changelist")
        response = self.client.get(url)
        self.assertContains(response, "Title")

    # integration
    def test_display_field_description(self) -> None:
        url = self.make_url(AdminSite(), Module, "changelist")
        response = self.client.get(url)
        self.assertContains(response, "Description")

    # integration
    def test_context_queryset(self) -> None:
        url = self.make_url(AdminSite(), Module, "changelist")
        response = self.client.get(url)
        queryset = self.get_queryset(response)
        self.assertEqual([self.module2, self.module], [*queryset.all()])

    # integration
    def test_short_description(self) -> None:
        module_admin = ModuleAdmin(Module, AdminSite())
        short_description = module_admin.description(self.module)
        self.assertLessEqual(len(short_description), 30)

    # integration
    def test_course_title(self) -> None:
        module_admin = ModuleAdmin(Module, AdminSite())
        course_title = module_admin.course_title(self.module)
        self.assertLessEqual(self.course.title, course_title)

    @staticmethod
    def _get_filtered_module_count(**kwargs) -> int:
        return Module.objects.filter(**kwargs).count()

    # integration
    def test_add_module(self) -> None:
        before_module_count = self._get_filtered_module_count(title="CCourse")

        add_url = self.make_url(self.site, Module, "add")
        response = self.client.post(
            add_url,
            data={
                "title": "CCourse",
                "slug": "c_course",
                "course": self.course.id,
            },
        )
        change_list_url = self.make_url(self.site, Module, "changelist")
        self.assertRedirects(response, change_list_url)

        after_module_count = self._get_filtered_module_count(title="CCourse")
        self.assertEqual(after_module_count, before_module_count + 1)

    # integration
    def test_change_subject(self) -> None:
        before_module_count = self._get_filtered_module_count(title="CCourse")

        change_url = self.make_url(
            self.site, Module, "change", self.module.id
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
                "course": self.course.id,
            },
        )
        change_list_url = self.make_url(
            self.site, Module, "changelist"
        )  # abstract layer
        self.assertRedirects(response, change_list_url)

        after_module_count = self._get_filtered_module_count(title="Course")
        self.assertEqual(after_module_count, before_module_count + 1)
