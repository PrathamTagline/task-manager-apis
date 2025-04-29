from django.contrib import admin
from .models import Task, TaskComment, TaskIssue, SubTask
# Register your models here.

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'key', 'status', 'priority', 'created_at')
    search_fields = ('title', 'key')
    list_filter = ('status', 'priority', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('key', 'created_at')

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'key', 'status', 'created_at')
    search_fields = ('title', 'key')
    list_filter = ('status', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('key', 'created_at')

@admin.register(TaskComment)
class TaskCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'user', 'created_at')
    search_fields = ('task__title', 'user__username')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

@admin.register(TaskIssue)
class TaskIssueAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'user', 'created_at')
    search_fields = ('task__title', 'user__username')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)