from django.urls import path
from . import views
urlpatterns = [
    path('task/list/', views.TackListView.as_view(), name="task-list" ),
    path("task/detail/<int:pk>", views.TaskDetailView.as_view(), name="task-detail")
]