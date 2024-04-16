from django.test import TestCase
from django.utils import timezone
from user.models import NilvaUser
from .models import Task


class TaskModelTestCase(TestCase):
    def setUp(self):
        self.user = NilvaUser.objects.create(username='RandomUserName',password="TestPassWord")
        self.task = Task.objects.create(title='My lovely task',
                    description='This task is for test and have no other usage',
                    assigned_to=self.user,
                    due_datetime=timezone.now() + timezone.timedelta(days=1))
    def task_task_creation(self):
        self.assertEqual(self.task.title,'My lovely task')
        self.assertEqual(self.task.assigned_to,self.user)
    