from django.contrib import admin

from apps.courses.models import Subject


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    pass
