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
        cls.user = user = User.objects.create_superuser(
            username=settings.DEFAULT_ADMIN_NAME,
            email=settings.DEFAULT_ADMIN_EMAIL,
            password=settings.DEFAULT_ADMIN_PASSWORD,
        )
        cls.course = course = Course.objects.create(
            title='Course1',
            owner=user,
        )
        cls.module = Module.objects.create(
            title='Module1',
            course=course,
            description='Best description' * 10,
        )
        cls.module2 = Module.objects.create(
            title='Module2',
            course=course,
            description='Best description' * 10,
        )

    # integration
    def test_module_is_displayed(self) -> None:
        url = self.make_url(AdminSite(), Module, 'changelist')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    # integration
    def test_display_field_title(self) -> None:
        url = self.make_url(AdminSite(), Module, 'changelist')
        response = self.client.get(url)
        self.assertContains(response, 'Title')

    # integration
    def test_display_field_description(self) -> None:
        url = self.make_url(AdminSite(), Module, 'changelist')
        response = self.client.get(url)
        self.assertContains(response, 'Description')

    # integration
    def test_context_queryset(self) -> None:
        url = self.make_url(AdminSite(), Module, 'changelist')
        response = self.client.get(url)
        queryset = response.context['cl'].queryset

        self.assertEqual([self.module2, self.module], [*queryset.all()])

    # integration
    def test_reduced_description(self) -> None:
        module_admin = ModuleAdmin(Module, AdminSite())
        reduced_description = module_admin.description(self.module)

        self.assertLessEqual(len(reduced_description), 30)

    # integration
    def test_course_title(self) -> None:
        module_admin = ModuleAdmin(Module, AdminSite())
        course_title = module_admin.course_title(self.module)

        self.assertLessEqual(self.course.title, course_title)
