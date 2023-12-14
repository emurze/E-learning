import copy

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import transaction

from apps.courses.models import Module, Course
from utils.tests.base import BaseTestCase

User = get_user_model()


class ModuleModelTestCase(BaseTestCase):
    """
    id: bigint ( Primary Key, auto-gen )

    title: varchar ( maxlength, Not Null )

    description: text

    course: Course ( Foreign Key, Not Null )

    __str__ contains module ( title ) and course ( title )
    """

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(
            username=settings.DEFAULT_ADMIN_NAME,
            password=settings.DEFAULT_ADMIN_PASSWORD,
        )
        cls.course = Course.objects.create(
            title='Course1',
            owner=user,
        )

    # integration
    def test_id_is_pk(self) -> None:
        module = Module.objects.create(title='Hi', course=self.course)
        self.assertEqual(module.pk, module.id)

    # integration
    def test_id_auto_generation(self) -> None:
        module = Module(title='Hi', course=self.course)
        self.assertFalse(module.id)

        module.save()
        self.assertTrue(module.id)

    # integration
    def test_title_maxlength(self) -> None:
        module = Module(title='H' * 128, course=self.course)
        module.full_clean()

        with self.assertRaises(ValidationError):
            module = Module(title='H' * 129, course=self.course)
            module.full_clean()

    # integration
    def test_title_not_null(self) -> None:
        with self.assertRaises(ValidationError):
            module = Module(course=self.course)
            module.full_clean()

    # integration
    def test_description_existence(self) -> None:
        module = Module(title='.', description='hi', course=self.course)
        module.full_clean()

    # integration
    def test_course_fk_not_null(self) -> None:
        with self.assertRaises(ValidationError):
            module = Module(title='.', )
            module.full_clean()

    # integration
    def test_course_fk_rel_name(self) -> None:
        module1 = Module.objects.create(title='.', course=self.course)
        module2 = Module.objects.create(title='..', course=self.course)

        self.assertEqual([module1, module2], list(self.course.modules.all()))

    # integration
    def test_course_fk_on_delete(self) -> None:
        module1 = Module.objects.create(title='.', course=self.course)

        self.assertEqual([module1], list(self.course.modules.all()))

        with transaction.atomic():
            _id = copy.copy(self.course.id)
            sid = transaction.savepoint()

            self.course.delete()

            with self.assertRaises(module1.DoesNotExist):
                module1.refresh_from_db()

            transaction.savepoint_rollback(sid)
            self.course.id = _id

        self.assertEqual([module1], list(self.course.modules.all()))

    # integration
    def test_magic_str(self) -> None:
        module1 = Module.objects.create(title='.', course=self.course)

        self.assertIn(module1.title, str(module1))
        self.assertIn(self.course.title, str(module1))
