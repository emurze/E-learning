# Generated by Django 4.2.8 on 2023-12-12 20:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Course",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=128)),
                ("slug", models.SlugField(max_length=128, unique=True)),
            ],
        ),
        migrations.DeleteModel(
            name="Module",
        ),
        migrations.AlterField(
            model_name="subject",
            name="slug",
            field=models.SlugField(max_length=128, unique=True),
        ),
    ]
