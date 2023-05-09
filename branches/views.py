from django.contrib import messages
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView
from base.decorators import superuser_required
from .models import Branch
from users.models import User
from .forms import BranchForm


# Create your views here.


class BranchCreateView(LoginRequiredMixin, CreateView):
    model = Branch
    template_name = 'branches/create-branch.html'
    form_class = BranchForm
    context_object_name = 'obj'
    success_message = 'La sucursal ha sido creado satisfactoriamente'
    success_url = reverse_lazy('branch-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        form.save()
        return response


@method_decorator(superuser_required, name='dispatch')
class BranchListView(LoginRequiredMixin, ListView):
    model = Branch
    context_object_name = 'obj'
    template_name = 'branches/branch-list.html'


@method_decorator(superuser_required, name='dispatch')
class BranchDetailView(LoginRequiredMixin, DetailView):
    model = Branch
    template_name = 'branches/branch-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        branch = self.get_object()
        context['obj'] = self.get_object()
        context['employees'] = branch.employees.all()
        if branch.manager:
            context['manager'] = branch.manager
        return context


@superuser_required
def disable_branch(request, pk):
    branch = get_object_or_404(Branch, pk=pk)
    context = {'obj': branch}
    template_name = 'branches/disable-branch.html'
    if request.method == 'POST':
        branch.is_active = False
        branch.save()
        messages.warning(request, 'La sucursal ha sido desactivada')
        return redirect('branch-list')
    return render(request, context, template_name)


@superuser_required
def activate_branch(request, pk):
    branch = get_object_or_404(Branch, pk=pk)
    context = {'obj': branch}
    template_name = 'branches/activate-branch.html'
    if request.method == 'POST':
        branch.is_active = True
        branch.save()
        messages.warning(request, 'La sucursal ha sido desactivada')
        return redirect('branch-list')
    return render(request, context, template_name)
