from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone


class Task(models.Model):
    """A task owned by one user, either Deep Work or Shallow Work."""

    TYPE_CHOICES = [('deep', 'Deep Work'), ('shallow', 'Shallow Work')]
    PRIORITY_CHOICES = [('low', 'Low'), ('medium', 'Medium'), ('high', 'High')]
    STATUS_CHOICES = [('todo', 'To do'), ('doing', 'In progress'), ('done', 'Done')]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks'
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    task_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='deep')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='todo')
    image = models.ImageField(upload_to='tasks/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def str(self):
        return self.title


class FocusSession(models.Model):
    """One finished focus session linked to a task."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sessions'
    )
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='sessions')
    minutes = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(240)]
    )
    started_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-started_at']

    def str(self):
        return f'{self.task.title} - {self.minutes} min'
