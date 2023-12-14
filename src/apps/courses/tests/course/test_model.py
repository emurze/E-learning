import copy
from pprint import pprint

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models.signals import pre_save

from apps.courses.models import Course, Subject
from utils.tests.base import BaseTestCase, User


class CourseModelTestCase(BaseTestCase):
    """
    owner: fk User
    title: str
    slug: str auto-gen
    subject: fk Subject
    description: text
    created: date auto-gen

    ordering by -created
    """

    login_username: str = "vladik"
    login_password: str = "12345678"

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create_user(
            username=cls.login_username,
            password=cls.login_password,
        )

    # integration
    def test_title_maxlength(self) -> None:
        course = Course(title="s" * 128, owner=self.user)
        pre_save.send(
            sender=Course,  # generates slug implicitly
            instance=course,
        )
        course.full_clean()

        with self.assertRaises(ValidationError):
            course2 = Course(title="s" * 129, owner=self.user)
            pre_save.send(
                sender=Course,  # generates slug implicitly
                instance=course2,
            )
            course2.full_clean()

    # integration
    def test_title_not_null(self) -> None:
        with self.assertRaises(ValidationError):
            course = Course()
            course.full_clean()

    # integration
    def test_slug_maxlength(self) -> None:
        course = Course(title='.', slug='s' * 128, owner=self.user)
        course.full_clean()

        with self.assertRaises(ValidationError):
            course2 = Course(title=".", slug='s' * 129, owner=self.user)
            course2.full_clean()

    # integration
    def test_slug_constraint(self) -> None:
        with self.assertRaises(ValidationError):
            course2 = Course(title=".", slug='s[]', owner=self.user)
            course2.full_clean()

    # integration
    def test_slug_auto_generation(self) -> None:
        course = Course(title="weF", owner=self.user)
        course.save()
        self.assertEqual('wef', course.slug)

    # integration
    def test_slug_unique(self) -> None:
        course = Course(title="weF", slug=1, owner=self.user)
        course.save()

        with self.assertRaises(ValidationError):
            course2 = Course(title="weF", slug=1, owner=self.user)
            course2.full_clean()

    # integration
    def test_magic_str(self) -> None:
        course = Course(title="weFWE", owner=self.user)
        self.assertIn(course.title, str(course))

    # integration
    def test_fk_subject(self) -> None:
        subject = Subject.objects.create(title='Math')
        course = Course.objects.create(
            title='Course',
            subject=subject,
            owner=self.user,
        )
        self.assertEqual(course.subject, subject)

    # integration
    def test_fk_subject_rel_name(self) -> None:
        subject = Subject.objects.create(title='Math')
        course1 = Course.objects.create(
            title='Course1',
            subject=subject,
            owner=self.user,
        )
        course2 = Course.objects.create(
            title='Course2',
            subject=subject,
            owner=self.user,
        )
        self.assertEqual(list(subject.courses.all()), [course2, course1])

    # integration
    def test_fk_subject_on_delete(self) -> None:
        subject = Subject.objects.create(title='Math')
        course1 = Course.objects.create(
            title='Course1',
            subject=subject,
            owner=self.user,
        )
        self.assertEqual(course1.subject, subject)

        subject.delete()
        course1.refresh_from_db()

        self.assertEqual(course1.subject, None)

    # integration
    def test_description_null(self) -> None:
        course = Course.objects.create(title='Math', owner=self.user)
        self.assertEqual(course.description, None)

    # integration
    def test_created_auto_generation(self) -> None:
        course = Course(title='Math', owner=self.user)
        self.assertIs(course.created, None)

        course.save()
        self.assertIsNot(course.created, None)

    # integration
    def test_fk_owner(self) -> None:
        course1 = Course.objects.create(title='Course1', owner=self.user)
        self.assertEqual(course1.owner, self.user)

    # integration
    def test_fk_owner_rel_name(self) -> None:
        course1 = Course.objects.create(title='Course1', owner=self.user)
        course2 = Course.objects.create(title='Course2', owner=self.user)

        self.assertEqual(list(self.user.courses.all()), [course2, course1])

    # integration
    def test_fk_owner_on_delete(self) -> None:
        course1 = Course.objects.create(title='Course1', owner=self.user)
        course2 = Course.objects.create(title='Course2', owner=self.user)

        self.assertEqual(list(self.user.courses.all()), [course2, course1])

        with transaction.atomic():
            _id = copy.copy(self.user.id)
            sid = transaction.savepoint()

            self.user.delete()

            with self.assertRaises(course1.DoesNotExist):
                course1.refresh_from_db()

            with self.assertRaises(course2.DoesNotExist):
                course2.refresh_from_db()

            transaction.savepoint_rollback(sid)
            self.user.id = _id

        self.assertEqual(list(self.user.courses.all()), [course2, course1])

    # integration
    def test_reversed_ordering(self) -> None:
        course1 = Course.objects.create(title='Course1', owner=self.user)
        course2 = Course.objects.create(title='Course2', owner=self.user)

        courses = Course.objects.all()

        self.assertTrue(courses.ordered)
        self.assertEqual([course2, course1], list(courses))
