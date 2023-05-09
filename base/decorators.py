from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect
from functools import wraps

from django.views.generic import FormView


# Create your views here.


def superuser_required(function):
    @wraps(function)
    @user_passes_test(lambda user: user.is_superuser)
    def wrap(request, *args, **kwargs):
        response = function(request, *args, **kwargs)
        # Add 'form' attribute to the view if it doesn't exist
        if isinstance(response, FormView) and not hasattr(response, 'form'):
            response.form = None
        return response
    return wrap


def activate_or_deactivate_state(model):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            pk = kwargs.get('pk')
            obj = get_object_or_404(model, pk=pk)
            if not obj.state:
                obj.state = True
                obj.save()
                return view_func(request, *args, **kwargs)
            else:
                not obj.state
                obj.state = False
                obj.save()
                return view_func(request, *args, **kwargs)
        return wrapped_view
    return decorator


"""def deactivate_state(model):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            pk = kwargs.get('pk')
            obj = get_object_or_404(model, pk=pk)
            if obj.state:
                obj.state = False
                obj.save()
            return view_func(request, *args, **kwargs)
        return wrapped_view
    return decorator"""
