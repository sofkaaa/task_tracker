from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .mixins import UserIsOwnerMixin

from .models import Task
from .forms import TaskForm
# Create your views here.

class TackListView(ListView):
    model = Task
    template_name = "tasks_list.html"

    def get_queryset(self):
        queryset = Task.objects.filter(status_ne = "done").exclude(a=True)
        return queryset

class TaskDetailView(DetailView):
    model = Task
    template_name = "task_detail.html"


class TaskCreateView(LoginRequiredMixin,CreateView):
    model = Task
    form_class = TaskForm
    template_name = "task_create.html"
    success_url = reverse_lazy("task-list")

    def form_valid(self, form):
        user = self.request.user
        print(user.username)
        form.instance.user = user

        return super().form_valid(form)
    
class TaskEditView(UserIsOwnerMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "task_create.html"
    success_url = reverse_lazy("task-list")    