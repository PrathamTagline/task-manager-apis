from django.contrib import admin
from .models import Project, ProjectMembership
# Register your models here.
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'key', 'created_by', 'created_at')
    search_fields = ('name', 'key')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    readonly_fields = ('key', 'created_at')

@admin.register(ProjectMembership)
class ProjectMembershipAdmin(admin.ModelAdmin):
    list_display = ('id', 'project', 'user', 'role', 'joined_at')
    search_fields = ('project__name', 'user__username')
    list_filter = ('role', 'joined_at',)
    ordering = ('joined_at',)
    readonly_fields = ('id', 'joined_at')