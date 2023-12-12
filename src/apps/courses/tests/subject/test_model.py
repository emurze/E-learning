from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save

from apps.courses.models import Subject
from utils.tests.base import BaseTestCase


class SubjectModelTestCase(BaseTestCase):
    """
    title: str
    slug: str auto-gen
    """

    # integration
    def test_title_not_null(self) -> None:
        with self.assertRaises(ValidationError):
            subject = Subject()
            subject.full_clean()

    # integration
    def test_title_maxlength(self) -> None:
        subject = Subject(title="s" * 128)
        pre_save.send(
            sender=Subject,  # generates slug implicitly
            instance=subject,
        )
        subject.full_clean()

        with self.assertRaises(ValidationError):
            subject2 = Subject(title="s" * 129)
            pre_save.send(
                sender=Subject,  # generates slug implicitly
                instance=subject2,
            )
            subject2.full_clean()

    # integration
    def test_slug_maxlength(self) -> None:
        subject = Subject(title=".", slug="s" * 128)
        subject.full_clean()

        with self.assertRaises(ValidationError):
            subject = Subject(title=".", slug="s" * 129)
            subject.full_clean()

    # integration
    def test_slug_constraint(self) -> None:
        with self.assertRaises(ValidationError):
            subject = Subject(title='.', slug="sEF[]")
            subject.full_clean()

    # integration
    def test_slug_auto_generation(self) -> None:
        subject = Subject(title="weF")
        subject.save()
        self.assertEqual('wef', subject.slug)

    # integration
    def test_slug_unique(self) -> None:
        subject = Subject(title="weF", slug=1)
        subject.save()

        with self.assertRaises(ValidationError):
            subject2 = Subject(title="weF", slug=1)
            subject2.full_clean()

    # integration
    def test_magic_str(self) -> None:
        subject = Subject(title="weFWE")
        self.assertIn(subject.title, str(subject))
