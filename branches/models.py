from django.db import models
from base.models import BaseModel
from users.models import User
from inventario.models import Products, Category, MeasureUnite, SubCategory


# Create your models here.
class Branch(BaseModel):
    name = models.CharField(max_length=50, verbose_name='Nombre')
    address = models.CharField(max_length=50, verbose_name='Direccion')
    phone = models.BigIntegerField(verbose_name='Telefono')
    description = models.TextField(verbose_name='Descripción')
    image = models.ImageField(upload_to='', blank=True, null=True)
    manager = models.OneToOneField(User, on_delete=models.CASCADE)
    state = models.BooleanField(default=True, verbose_name='Estado')
    employees = models.ManyToManyField(User, related_name='branches')

    class Meta:
        verbose_name = 'Sucursal'
        verbose_name_plural = 'Sucursales'

    def __str__(self):
        return self.name


class Inventory(BaseModel):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name="Nombre")
    code = models.CharField(max_length=30, unique=True, verbose_name="Codigo")
    image = models.ImageField(upload_to='products/')
    description = models.CharField(max_length=100, verbose_name="Descripción")
    stock = models.IntegerField(verbose_name="Cantidad")
    price = models.IntegerField(verbose_name="Precio")
    brand = models.CharField(max_length=100, verbose_name="Marca")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Categoria")
    unite_measure = models.ForeignKey(MeasureUnite, on_delete=models.CASCADE, verbose_name="Unidad de Medida")
    expired = models.DateField('Fecha de Caducidad', blank=True, null=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, verbose_name="Sub Categoria")

    class Meta:
        verbose_name = 'Inventario'
        verbose_name_plural = 'Inventarios'

    def __str__(self):
        return self.branch and self.name


# Lleva un registro de las tranferencias


class Transfer(BaseModel):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    transfer_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f'{self.quantity} {self.product.name} transferido a {self.branch.name} el {self.transfer_date}'


class CashRegister(BaseModel):
    branch = models.OneToOneField(Branch, on_delete=models.CASCADE, name='cash_register',
                                  verbose_name='Sucursal')
    opening_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Monto de Apertura')
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Monto Actual')
    opened_at = models.DateTimeField(auto_now_add=True, verbose_name='Hora de Apertura')
    closed_at = models.DateTimeField(blank=True, null=True, verbose_name='Hora de Cierre')

    # Agregar funcion para calcular el cash final entre las dos horas de apertura y cierre
