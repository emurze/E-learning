import reprlib

from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet

from apps.courses.models import Subject, Module


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    def get_queryset(self, request: WSGIRequest) -> QuerySet:
        queryset = super().get_queryset(request)
        return queryset.select_related('course')

    @staticmethod
    def description(instance: Module) -> str:
        return reprlib.repr(instance.description)

    @staticmethod
    def course_title(instance: Module) -> str:
        return instance.course.title

    list_display = ('title', description, course_title)
