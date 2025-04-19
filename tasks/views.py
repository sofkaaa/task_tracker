from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .mixins import UserIsOwnerMixin

from .models import Task, Coment
from .forms import TaskForm, CommentForm
# Create your views here.

class TaskListView(ListView):
    model = Task
    template_name = "tasks_list.html"

    def get_queryset(self):
        queryset = Task.objects.exclude(status="done").exclude(description=True)
        return queryset

class TaskDetailView(DetailView):
    model = Task
    template_name = 'task_detail.html' 
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context
    
    def post(self, request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            form = CommentForm(request.POST, request.FILES)

            if form.is_valid():
                new_coment:Coment = form.instance
                new_coment.task = self.get_object()
                new_coment.user = self.request.user
                new_coment.save()

            return redirect(request.path_info)
        else: 
            return HttpRequest(content = "Must bt authenticated", status = 403)
  

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


class ComentEditView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = Coment
    form_class = CommentForm
    template_name = "coment_edit.html"

    def get_success_url(self):
        return reverse("task-detail", kwargs={"pk": self.get_object().pk}) 


class ComentDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = Coment
    template_name = "coment_delete.html"

    def get_success_url(self):
        return reverse_lazy("task-detail", kwargs={"pk": self.get_object().pk})
    
