from .models import User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import UserForm, CustomUserCreationForm
from base.decorators import superuser_required, activate_or_deactivate_state
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import  get_object_or_404, render, redirect


# Create your views here.


@method_decorator(superuser_required, name='dispatch')
class UsersList(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users-list.html'
    form_class = UserForm
    context_object_name = 'obj'
    login_url = ('login/')

@method_decorator(superuser_required, name='dispatch')
class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'user-detail.html'
    context_object_name = 'obj'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        branches = user.branches.all()
        context['branches'] = branches
        return context


class UserCreationView(LoginRequiredMixin, CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'user-create.html'
    success_url = reverse_lazy('users-list')
    login_url = ('login/')

    @method_decorator(superuser_required, name='dispatch')
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Verificar si el nombre de usuario ya existe
        if User.objects.filter(username=form.cleaned_data['username']).exists():
            form.add_error('username', 'Este nombre de usuario ya está en uso.')
            return self.form_invalid(form)
        else:
            form.save()
            return super().form_valid(form)


@login_required(login_url='/login/')
@superuser_required
def disable_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    context = {'obj': user}
    template_name = 'confirm-disable-user.html'
    if request.method == 'POST':
        user.is_active = False
        user.save()
        messages.warning(request, 'Usuario Desactivado')
        return redirect('users-list')
    return render(request, template_name, context)


@login_required(login_url='/login/')
@superuser_required
def activate_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    context = {'obj': user}
    template_name = 'confirm-activate-user.html'
    if request.method == 'POST':
        user.is_active = True
        user.save()
        messages.warning(request, 'Usuario Activado')
        return redirect('users-list')
    return render(request, template_name, context)

@method_decorator(superuser_required, name='dispatch')
class UserUpdate(LoginRequiredMixin, UpdateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'user-create.html'
    context_object_name = 'obj'
    success_message = 'El usuario ha sido actualizado'
    success_url = reverse_lazy('users-list')

    def form_valid(self, form):
        self.object = self.request.user.pk
        return super().form_valid(form)












