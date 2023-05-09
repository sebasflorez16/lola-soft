from django.urls import path
from .views import UsersList, UserCreationView, UserUpdate, UserDetailView
from . import views

urlpatterns = [
    path('users/', UsersList.as_view(), name='users-list'),
    path('users/create/', UserCreationView.as_view(), name='users-create'),
    path('users/detail/<int:pk>', UserDetailView.as_view(), name='user-detail'),
    path('users/update/<int:pk>/', UserUpdate.as_view(), name='user-update'),
    path('users/deactivate/<int:pk>/', views.disable_user, name='disable-user'),
    path('users/activate/<int:pk>/', views.activate_user, name='activate-user'),

]
