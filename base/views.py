
from django.views.generic import TemplateView
from django.contrib.auth.views import FormView
from django.contrib.auth.mixins import LoginRequiredMixin


class Home(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'


class LoginView(FormView):
    template_name = 'login.html'
