from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.urls import reverse_lazy
from base.decorators import superuser_required
from .models import *
from .forms import CompanyCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView


# Create your views here.


class CompanyListView(LoginRequiredMixin, ListView):
    model = Company
    template_name = 'companies/companies-list.html'
    context_object_name = 'obj'


@method_decorator(superuser_required, name='dispatch')
class CompanyCreateView(LoginRequiredMixin, CreateView):
    model = Company
    form_class = CompanyCreateForm
    template_name = 'companies/company-form.html'
    success_url = reverse_lazy('companies-list')
    success_messages = "Empresa creada correctamente"
    context_object_name = 'obj'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def dispatch(self, *args, **kwargs):
        print('vista dispatch')
        return super().dispatch(*args, **kwargs)


@login_required(login_url='/login/')
@superuser_required
def disable_company(request, pk):
    company = get_object_or_404(Company, pk=pk)
    context = {'obj': company}
    template_name = 'companies/confirm-disable-company.html'
    if request.method == 'POST':
        company.is_active = False
        company.save()
        messages.warning(request, 'Usuario Desactivado')
        return redirect('companies-list')
    return render(request, template_name, context)


@login_required(login_url='/login/')
@superuser_required
def activate_company(request, pk):
    company = get_object_or_404(Company, pk=pk)
    context = {'obj': company}
    template_name = 'companies/confirm-activate-company.html'
    if request.method == 'POST':
        company.is_active = True
        company.save()
        messages.warning(request, 'Usuario Activado')
        return redirect('companies-list')
    return render(request, template_name, context)


class CompanyDetail(LoginRequiredMixin, DetailView):
    model = Company
    template_name = 'companies/companies-detail.html'
    context_object_name = 'obj'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['obj'] = self.get_object()
        return context
