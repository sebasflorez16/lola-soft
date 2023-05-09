from django.urls import path
from .views import BranchCreateView, BranchListView, BranchDetailView
from . import views

urlpatterns = [
    path('branch/list/', BranchListView.as_view(), name='branch-list'),
    path('branch/create/', BranchCreateView.as_view(), name='branch-create'),
    path('branch/detail/<int:pk>/', BranchDetailView.as_view(), name='branch-detail'),

    # Activar/Desactivar las sucursales
    path('branch/activate-branch/<int:pk>', views.activate_branch, name='activate-branch'),
    path('branch/disable-branch/<int:pk>', views.disable_branch, name='disable-branch'),

]
