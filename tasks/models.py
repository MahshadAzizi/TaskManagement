from enum import Enum

from django.db import models

from users.models import User


class TaskStatus(Enum):
    TO_DO = 'To Do'
    IN_PROGRESS = 'In Progress'
    REVIEW = 'Review'
    COMPLETED = 'Completed'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class Task(models.Model):
    assigner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks')
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_to_me_tasks', blank=True,
                                 null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=11, choices=TaskStatus.choices, default=TaskStatus.TO_DO.value)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
