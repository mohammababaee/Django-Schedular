from celery import shared_task
from django.core.mail import send_mail
from .models import Task

@shared_task
def send_task_email(task_id):
    task = Task.objects.get(id=task_id)
    recipient_email = task.assigned_to.email
    subject = "Do your Task!"
    message = f"Hi {task.assigned_to.username},\n\nThis is a reminder for your task: {task.title}.\n\nThe due date was : {task.due_datetime}.\n\nBest regards,\n"
    sender_email = "example@example.com"
    send_mail(subject, message, sender_email, [recipient_email])