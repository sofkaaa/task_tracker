from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Task
# Create your views here.

class TackListView(ListView):
    model = Task
    template_name = "tasks_list.html"

class TaskDetailView(DetailView):
    model = Task
    template_name = "task_detail.html"