from django.urls import path
from . import views
urlpatterns = [
    path("", views.TaskListView.as_view()),
    path("task/create/", views.TaskCreateView.as_view(), name="task-create"),
    path('task/list/', views.TaskListView.as_view(), name="task-list" ),
    path("task/detail/<int:pk>", views.TaskDetailView.as_view(), name="task-detail"),
    path("task/edit/<int:pk>", views.TaskEditView.as_view(), name = "task-edit"),
    path("task/delete/<int:pk>", views.TaskDeleteView.as_view(), name="task-delete")

]