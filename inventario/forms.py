from django import forms
from .models import Products


class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        description = forms.CharField(widget=forms.TextInput)
        fields = [
            'name',
            'code',
            'description',
            'stock',
            'price',
            'brand',
            'category',
            'unite_measure',
            'expired',
            'subcategory',
            'barcode',
            'is_active',
        ]
        widget = {'description': forms.TextInput()}
