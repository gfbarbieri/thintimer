from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
from datetime import timedelta

# Create your models here.

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    total_time_spent = models.DurationField(default=timedelta(seconds=0))
    tags = models.CharField(max_length=255, null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Entry(models.Model):
    task = models.ForeignKey('Task', on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.task.total_time_spent = F('total_time_spent') + self.total_time()
        self.task.save(update_fields=['total_time_spent'])

    def delete(self, *args, **kwargs):
        self.task.total_time_spent = F('total_time_spent') - self.total_time()
        self.task.save(update_fields=['total_time_spent'])
        super().delete(*args, **kwargs)

    def total_time(self):
        return self.end_time - self.start_time