from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.utils import timezone
from user.models import NilvaUser
from .models import Task


class TaskModelTestCase(TestCase):
    def setUp(self):
        self.user = NilvaUser.objects.create(
            username="testuser", email="test@example.com"
        )

    def test_task_creation(self):
        title = "Test Task"
        description = "This is a test task description."
        due_datetime = timezone.now() + timezone.timedelta(days=1)
        task = Task.objects.create(
            title=title,
            description=description,
            assigned_to=self.user,
            due_datetime=due_datetime,
        )
        self.assertEqual(task.title, title)
        self.assertEqual(task.description, description)
        self.assertEqual(task.assigned_to, self.user)
        self.assertEqual(task.due_datetime, due_datetime)
        self.assertEqual(task.notification_status, Task.NOT_NOTIFIED)
        self.assertIsNone(task.notification_datetime)
        self.assertFalse(task.pre_tasks.exists())

    def test_task_str_method(self):
        title = "Test Task"
        task = Task.objects.create(
            title=title,
            description="Test description",
            assigned_to=self.user,
            due_datetime=timezone.now(),
        )
        self.assertEqual(str(task), f"Task {title} For {self.user}")


class CheckTaskValidationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("task_validation")

    def test_no_tasks_provided(self):
        data = {}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "No tasks provided")

    def test_invalid_tasks_order(self):
        data = {
            "tasks": [
                {
                    "id": 1,
                    "title": "task 1",
                    "description": "desc 1",
                    "owner": "nilva.man",
                    "time_to_send": "2020-05-10T10:30:00Z",
                    "pre_tasks": [],
                },
                {
                    "id": 2,
                    "title": "task 2",
                    "description": "desc 2",
                    "owner": "nilva.man",
                    "time_to_send": "2020-05-06T10:30:00Z",
                    "pre_tasks": [1, 3],
                },
                {
                    "id": 3,
                    "title": "task 3",
                    "description": "desc 3",
                    "owner": "nilva.man",
                    "time_to_send": "2020-02-10T09:30:00Z",
                    "pre_tasks": [],
                },
            ]
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "No")

    def test_valid_tasks_order(self):
        data = {
            "tasks": [
                {
                    "id": 1,
                    "title": "task 1",
                    "description": "desc 1",
                    "owner": "nilva.man",
                    "time_to_send": "2020-05-10T10:30:00Z",
                    "pre_tasks": [],
                },
                {
                    "id": 2,
                    "title": "task 2",
                    "description": "desc 2",
                    "owner": "nilva.man",
                    "time_to_send": "2020-06-10T12:30:00Z",
                    "pre_tasks": [1, 3],
                },
                {
                    "id": 3,
                    "title": "task 3",
                    "description": "desc 3",
                    "owner": "nilva.man",
                    "time_to_send": "2020-06-01T12:30:00Z",
                    "pre_tasks": [1],
                },
            ]
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "Yes")

    def test_missing_pre_task(self):
        data = {
            "tasks": [
                {"id": 1, "time_to_send": "2023-04-17T10:00:00Z", "pre_tasks": []},
                {
                    "id": 2,
                    "time_to_send": "2023-04-17T11:00:00Z",
                    "pre_tasks": [1, 100],
                },
                {"id": 3, "time_to_send": "2023-04-17T12:00:00Z", "pre_tasks": [2]},
            ]
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "Yes")
