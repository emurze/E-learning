from django.utils.text import slugify


def generate_title(sender, **kwargs) -> None:
    instance = kwargs.get("instance")
    if instance.slug == "":
        instance.slug = slugify(instance.title)
