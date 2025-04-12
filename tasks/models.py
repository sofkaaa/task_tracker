from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=50, verbose_name="task`s titele")
    description = models.TextField(verbose_name = "description of the task")
    
    STATUS_CHOISES = [
            ("in_prog", "In Progress"),
            ("done", "Done"),
            ("delayed", "Delayed"),
            ("not_start", "Not Started"),
    ]
    
    status = models.CharField(max_length=10, choices=STATUS_CHOISES, default="not_start")

    PRIORITY_CHOISES = {
        "low": "Low Priority",
        "min": "Medium Priority",
        "high": "High Priority",
    }

    priority = models.CharField(max_length=5, choices=PRIORITY_CHOISES, default="mid")

    due_to = models.DateTimeField(null= True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Coment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_ad = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(null=True, auto_now=True)