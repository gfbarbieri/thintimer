from rest_framework import serializers

from .models import Task
from .models import Entry

class TaskSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Task
        fields = ('id', 'name', 'description', 'total_time_spent', 'tags', 'user', 'created_at', 'updated_at')

class EntrySerializer(serializers.ModelSerializer):
    task_name = serializers.ReadOnlyField(source='task.name')
    total_time = serializers.SerializerMethodField()

    class Meta:
        model = Entry
        fields = ['id', 'task', 'task_name', 'start_time', 'end_time', 'total_time']

    def get_total_time(self, obj):
        return str(obj.end_time - obj.start_time)