from django.contrib import admin

from .models import Task, Comment


class TaskAdmin(admin.ModelAdmin):
    list_display = ["id", "title"]

class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", "user"]


admin.site.register(Task, TaskAdmin)
admin.site.register(Comment, CommentAdmin)