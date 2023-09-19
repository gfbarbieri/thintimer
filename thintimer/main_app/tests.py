###############################################################################
# IMPORTS
###############################################################################

# Standard library imports.
from datetime import timedelta

# Third-party imports: Django natives.
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

# Third-party imports: Django DRF.
from rest_framework import status
from rest_framework.test import APITestCase

# Local imports.
from main_app.models import Task

###############################################################################
# DRF API TEST CASES
###############################################################################

class TaskTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.url = reverse('task-list')
        Task.objects.create(name='Test Task 1', description='Test Description 1', user=self.user)
        Task.objects.create(name='Test Task 2', description='Test Description 2', user=self.user)

    def test_list_tasks(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_task(self):
        data = {'name': 'New Task', 'description': 'New Description'}
        response = self.client.post(self.url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 3)

class TaskUpdateTestCase(APITestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

        # Create a sample task
        self.task = Task.objects.create(
            name='Test Task',
            description='This is a test task',
            total_time_spent=timedelta(hours=0, minutes=0, seconds=0),
            tags='test, sample',
            user=self.user
        )

    def test_successful_task_update(self):
        url = reverse('task-detail', kwargs={'pk': self.task.id})
        data = {'name': 'New Task Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unsuccessful_task_update(self):
        url = reverse('task-detail', kwargs={'pk': self.task.id})
        data = {'name': ''}  # Name should not be empty
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
