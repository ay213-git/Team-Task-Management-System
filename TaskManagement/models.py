from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractUser


# מודל משתמש שמורש מ-User של Django
class User(AbstractUser):

    ROLE_CHOICES = [
        ('manager', 'מנהל'),
        ('worker', 'עובד'),
    ]

    team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='members')  # מפתח זר לצוות
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)

    def __str__(self):
        return self.username


# מודל צוות
class Team(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# מודל משימה
class Task(models.Model):
    STATUS_CHOICES = [
        ('new', 'חדש'),
        ('in_progress', 'בתהליך'),
        ('completed', 'הושלם'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='new')
    assigned_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='tasks')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
