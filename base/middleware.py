from django.shortcuts import redirect
from django.contrib.sessions.models import Session
from datetime import datetime, timedelta

timedelta


# Niega el acceso a usuarios no activos en la base de datos
class CheckUserActiveMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Obtener el usuario actual
        user = request.user

        # Verificar si el usuario está autenticado y si está desactivado
        if user.is_authenticated and not user.is_active:
            # Redirigir al usuario a una página de acceso denegado
            return redirect('login/')

        response = self.get_response(request)
        return response


# Elimina la sesion del usuario despues de un tiempo
class SessionIdleTimeout:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Verificar si el usuario está autenticado y es un superusuario
        if request.user.is_authenticated and request.user.is_superuser:
            # Obtener la sesión del usuario
            session_key = request.session.session_key
            if session_key is not None:
                session = Session.objects.get(pk=session_key)

                # Obtener la última actividad del usuario
                last_activity = session.get_decoded().get('_last_activity')

                # Verificar si ha pasado el tiempo de inactividad permitido
                if last_activity and datetime.now() - last_activity > timedelta(minutes=30):
                    # Desconectar la sesión del usuario
                    session.delete()
                    del request.session['_auth_user_id']
                    del request.session['_auth_user_backend']
        return response




