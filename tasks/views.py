from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .mixins import UserIsOwnerMixin

from .models import Task, Coment
from .forms import TaskForm, CommentForm


from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
# Create your views here.



class TaskListView(ListView):
    model = Task
    template_name = "tasks_list.html"
    context_object_name = 'task_list'

    def get_queryset(self):
        return Task.objects.all()

class TaskDetailView(DetailView):
    model = Task
    template_name = 'task_detail.html'
    context_object_name = 'task'
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


class UserRegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'registration/register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task-list')
        return render(request, 'registration/register.html', {'form': form})

class UserLoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('task-list')
        return render(request, 'login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

def golovna(request):
    recent_tasks = Task.objects.order_by('-due_to')[:3]  # Отримуємо 3 останні завдання
    # Додамо короткий опис для головної сторінки (можна заповнити в адмінці)
    for task in recent_tasks:
        if not task.description:
            task.short_description = "Короткий опис відсутній."
        elif len(task.description) > 100:
            task.short_description = task.description[:100] + "..."
        else:
            task.short_description = task.description
    return render(request, 'golovna.html', {'recent_tasks': recent_tasks})