from django.contrib import admin
from .models import Task, Entry

# Register your models here.

admin.site.register(Task)
admin.site.register(Entry)
