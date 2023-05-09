from django.urls import path
from .views import ProjectListView, ProyectCreatView, ProjectDetailView, TaskListView, TaskCreateView

urlpatterns = [
    path('project/', ProjectListView.as_view(), name='project-list'),
    path('project/create/', ProyectCreatView.as_view(), name='project-create'),
    path('project/detail/<int:pk>', ProjectDetailView.as_view(), name='project-detail'),
    path('project/task/', TaskListView.as_view(), name='task-list'),
    path('project/task/create', TaskCreateView.as_view(), name='task-create'),
]
