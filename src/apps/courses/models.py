from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify


class Subject(models.Model):
    title = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128)

    def __str__(self) -> str:
        return self.title


@receiver(pre_save, sender=Subject)
def generate_title(sender: Subject, **kwargs) -> None:
    instance = kwargs.get("instance")
    if instance.slug == "":
        instance.slug = slugify(instance.title)


class Module(models.Model):
    pass
