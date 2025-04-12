from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .mixins import UserIsOwnerMixin

from .models import Task
from .forms import TaskForm
# Create your views here.

class TaskListView(ListView):
    model = Task
    template_name = "tasks_list.html"

    def get_queryset(self):
        queryset = Task.objects.exclude(status="done").exclude(description=True)
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

    def get_success_url(self):
        url = reverse("task-detail", kwargs={"pk": self.get_object().pk})
        return url

class TaskDeleteView(UserIsOwnerMixin, DeleteView):
    model = Task
    template_name = "task_confirm_delete.html"
    success_url = reverse_lazy("task-list")
