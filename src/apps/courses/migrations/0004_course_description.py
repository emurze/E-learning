# Generated by Django 4.2.8 on 2023-12-12 21:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0003_course_subject"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
    ]
