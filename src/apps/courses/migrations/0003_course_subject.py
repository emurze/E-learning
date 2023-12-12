# Generated by Django 4.2.8 on 2023-12-12 20:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0002_course_delete_module_alter_subject_slug"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="subject",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="courses",
                to="courses.subject",
            ),
        ),
    ]
