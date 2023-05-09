from django.urls import path

from .views import ProductoCreate, ProductoList, CategoryListView
from . import views

urlpatterns = [
    path('products/', ProductoList.as_view(), name='product-list'),
    path('products/new/', ProductoCreate.as_view(), name='product-create'),
    # Category
    path('category/', CategoryListView.as_view(), name='category-list'),
    path('category/disable_category/<int:pk>/', views.disable_category, name='disable-category'),
    path('category/activate_state/<int:pk>/', views.activate_model, name='activate-model'),


]
