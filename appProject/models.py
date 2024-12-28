from django.db import models
from appAuth.models import User

class Project(models.Model):
        name = models.CharField(max_length=100, blank=False)
        description = models.TextField(max_length=300)
        owner = models.ForeignKey(User, on_delete=models.CASCADE)
        created_at = models.DateTimeField(auto_now_add=True)


        def __str__(self):
                return f"{self.name}"
        

class ProjectMember(models.Model):
        project = models.ForeignKey(Project, on_delete=models.CASCADE)
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        role = models.CharField(max_length=50, default="Member", blank=False)
        