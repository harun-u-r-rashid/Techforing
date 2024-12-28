from django.contrib import admin

from .models import Project, ProjectMember


class ProjectAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectMember)
