from django.contrib import admin

from .models import Task, FocusSession


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'task_type', 'priority', 'status', 'created_at')


@admin.register(FocusSession)
class FocusSessionAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'minutes', 'started_at')
