from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from apps.courses.signals import generate_title

User = get_user_model()


class Subject(models.Model):
    title = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128, unique=True)

    def __str__(self) -> str:
        return f'{self.__class__.__name__}(title={self.title})'


@receiver(pre_save, sender=Subject)
def subject_generate_title(sender: Subject, **kwargs) -> None:
    generate_title(sender, **kwargs)


class Course(models.Model):
    owner = models.ForeignKey(
        User,
        related_name='courses',
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128, unique=True)
    subject = models.ForeignKey(
        Subject,
        related_name='courses',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.__class__.__name__}(title={self.title})'


@receiver(pre_save, sender=Course)
def module_generate_title(sender: Course, **kwargs) -> None:
    generate_title(sender, **kwargs)
