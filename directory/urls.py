from django.urls import path
from .views import CompanyListView, CompanyCreateView, CompanyDetail
from . import views

urlpatterns = [
    path('companies/', CompanyListView.as_view(), name='companies-list'),
    path('companies/create/', CompanyCreateView.as_view(), name='companies-create'),
    path('companies/detail/<int:pk>/', CompanyDetail.as_view(), name='companies-detail'),
    path('companies/disable_company/<int:pk>/', views.disable_company, name='disable-company'),
    path('companies/activate_company/<int:pk>/', views.activate_company, name='activate-company'),
]
