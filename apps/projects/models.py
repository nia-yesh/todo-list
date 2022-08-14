from django.db import models

from apps.accounts.models import User


class Project(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    due_date = models.DateField(null=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.PROTECT, related_name='tasks')
    assignees = models.ManyToManyField(User)
    title = models.CharField(max_length=64)
    description = models.TextField()
    priority = models.PositiveIntegerField(null=True)
    deadline = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
