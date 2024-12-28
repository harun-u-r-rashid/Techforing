from django.db import models
from appAuth.models import User
from .constants import STATUS, PRIORITY
from appProject.models import Project


class Task(models.Model):
    title = models.CharField(max_length=100, blank=False)
    description = models.TextField(max_length=300, blank=False)
    status = models.CharField(max_length=100, default="TO DO", choices=STATUS)
    priority = models.CharField(max_length=100, default="LOW", choices=PRIORITY)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()

    def __str__(self):
        return f"{self.title}"


class Comment(models.Model):
    content = models.TextField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
