from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from base.decorators import superuser_required, activate_or_deactivate_state
from .models import Products, Category, MeasureUnite, SubCategory
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView
from .forms import ProductForm
from django.utils.decorators import method_decorator


# Create your views here.
class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'category'


class CategoryNew(LoginRequiredMixin, CreateView):
    model = Category
    template_name = 'category_form.html'
    context_object_name = 'obj'
    # form_class = CategoryForm
    success_url = reverse_lazy('inventario:category_list')
    success_message = "Categoria Creada Satisfactoriamente"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)


class CategoryEdit(LoginRequiredMixin, UpdateView):
    model = Category
    template_name = 'category_form.html'
    context_object_name = 'obj'
    # form_class = CategoryForm
    success_url = reverse_lazy('inventario:category_list')
    success_message = 'Categoria editada satisfactoriamente'


def form_valid(self, form):
    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)


@login_required(login_url='/login/')
@superuser_required
@activate_or_deactivate_state(Category)
def disable_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    context = {'obj': category}
    template_name = 'delete_confirm.html'
    if request.method == 'POST':
        category.state = False
        category.save()
        messages.warning(request, 'Categoria Inactivada')
        return redirect('category-list')
    return render(request, template_name, context)


@login_required(login_url='/login/')
@superuser_required
@activate_or_deactivate_state(Category)
def activate_model(request, pk):
    category = get_object_or_404(Category, pk=pk)
    context = {'obj': category}
    template_name = 'confirm_activate.html'

    if request.method == 'POST':
        if not category.state:
            category.state = True
            category.save()
            messages.success(request, 'Categoria Activada')
        return redirect('category-list')
    return render(request, template_name, context)


class ProductoList(LoginRequiredMixin, ListView):
    model = Products
    template_name = 'products_list.html'
    context_object_name = "obj"


class ProductoCreate(LoginRequiredMixin, CreateView):
    model = Products
    form_class = ProductForm
    template_name = 'product_new.html'
    success_url = reverse_lazy('products_list.html')
    success_message = 'Producto Agregado al Inventario'

    def form_valid(self, form):
        form.instance = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ProductoCreate, self).get_context_data(**kwargs)
        context['Categoria'] = Category.objects.all()
        context['Unidad de Medida'] = MeasureUnite.objects.all()
        context['Subcategoria'] = SubCategory.objects.all()
        return context
