from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.utils.text import slugify

from apps.courses.models import Subject
from utils.tests.base import BaseTestCase


class SubjectModelTestCase(BaseTestCase):
    """
    title: str
    slug: str auto-gen
    """

    # integration
    def test_title_max_length(self) -> None:
        subject = Subject(title="s" * 128)
        pre_save.send(sender=Subject, instance=subject)
        subject.full_clean()

        with self.assertRaises(ValidationError):
            subject2 = Subject(title="s" * 129)
            pre_save.send(
                sender=Subject,
                instance=subject2,
            )
            subject2.full_clean()

    def test_slug_max_length(self) -> None:
        subject = Subject(title=".", slug="s" * 128)
        subject.full_clean()

        with self.assertRaises(ValidationError):
            subject = Subject(title=".", slug="s" * 129)
            subject.full_clean()

    def test_slug_auto_generation(self) -> None:
        subject = Subject(title="weFWE")
        subject.save()
        self.assertEqual(slugify(subject.title), subject.slug)

    def test_magic_str(self) -> None:
        subject = Subject(title="weFWE")
        self.assertIn(subject.title, str(subject))
