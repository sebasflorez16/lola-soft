from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone

from .models import Project, Task
from django.views.generic import CreateView, ListView, DetailView
from django.utils.decorators import method_decorator
from base.decorators import superuser_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProjectForm, TaskForm


@method_decorator(superuser_required, name='dispatch')
class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'crew/project-list.html'
    context_object_name = 'project'


@method_decorator(superuser_required, name='dispatch')
class ProyectCreatView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'crew/project-create.html'
    success_url = 'project-list'

    def form_valid(self, form):
        # Verificar si el nombre de proyecto ya existe
        if Project.objects.filter(title=form.cleaned_data['title']).exists():
            form.add_error('title', 'Ya existe un proyecto con este nombre')
            return self.form_invalid(form)
        else:
            form.save()
            return super().form_valid(form)


@method_decorator(superuser_required, name='dispatch')
class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'crew/project-detail.html'
    context_object_name = 'obj'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        context["obj"] = self.get_object()
        tasks = project.tasks.all()  # Muestra la relacion M2M entre los dos modelos
        context["tasks"] = tasks
        if project.manager:
            context["manager"] = project.manager
        return context


@method_decorator(superuser_required, name='dispatch')
class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'crew/project-detail.html'
    context_object_name = 'task'

    def get_queryset(self):  # se ha actualizado para filtrar solo las tareas relacionadas con el proyecto en cuestión.
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        return Task.objects.filter(project=project)


@method_decorator(superuser_required, name='dispatch')
class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'crew/task-create.html'

    def get_success_url(self):
        return reverse_lazy('project-detail',
                            kwargs={'pk': self.object.project.pk})  # Retorna al proyecto al que se le asigno la tarea

    def form_valid(self, form):
        # Verificar si el nombre de la tarea ya existe
        if Project.objects.filter(title=form.cleaned_data['title']).exists():
            form.add_error('title', 'Ya existe una tarea con este nombre')
            return self.form_invalid(form)
        else:
            form.save()
            return super().form_valid(form)
