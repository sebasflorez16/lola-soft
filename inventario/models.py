from django.db import models
from simple_history.models import HistoricalRecords
from base.models import BaseModel
from directory.models import Providers
import random


class Category(BaseModel):
    description = models.CharField('Descripcion', max_length=50, blank=False, null=False, unique=True)
    state = models.BooleanField('Estado', default=True)
    historical = HistoricalRecords()

    @property
    def _history_user(self):  # Registra que usuario ha hecho el cambio
        return self.change_by

    @_history_user.setter
    def _history_user(self, value):
        self.change_by = value

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    # Indicador de oferta
    def __str__(self):
        return self.description


class SubCategory(BaseModel):
    description = models.CharField('Descripcion', max_length=50, blank=False, null=False, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    state = models.BooleanField('Estado', default=True)
    historical = HistoricalRecords()

    @property
    def _history_user(self):  # Registra que usuario ha hecho el cambio
        return self.change_by

    @_history_user.setter
    def _history_user(self, value):
        self.change_by = value

    class Meta:
        verbose_name = 'Subcategoria'
        verbose_name_plural = 'Subcategorias'

    def __str__(self):
        return self.description


class Indicator(BaseModel):
    descount_value = models.PositiveSmallIntegerField(default=0)
    category_product = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Indicador de Oferta')
    state = models.BooleanField('Estado', default=True)
    historical = HistoricalRecords()

    @property
    def _history_user(self):  # Registra que usuario ha hecho el cambio
        return self.change_by

    @_history_user.setter
    def _history_user(self, value):
        self.change_by = value

    class Meta:
        verbose_name = "Inidicador de Oferta"
        verbose_name_plural = "Inidicadores de Ofertas"

    def __str__(self):
        return f'Oferta de la categoria{self.category_product} : {self.descount_value}%'


# Clasifica como se almacena el modelo si son litros, litros etc
class MeasureUnite(BaseModel):
    description = models.CharField('Descripción', max_length=50, blank=False, null=False, unique=True)
    quantity = models.FloatField()
    price_measure = models.IntegerField()
    state = models.BooleanField('Estado', default=True)
    historical = HistoricalRecords()

    # Maneja el historial de los usuarions que han hecho cambios
    @property
    def _history_user(self):  # Registra que usuario ha hecho el cambio
        return self.change_by

    @_history_user.setter
    def _history_user(self, value):
        self.change_by = value

    # Calcula el precio de la unidad del producto
    @staticmethod
    def total_unit_price(self, product_id, measurement_unit_id):
        product = Products.objects.unit_price(product_id)
        measurement_unit = MeasureUnite.objects.unit_price(measurement_unit_id)
        total_unit = product * measurement_unit
        return total_unit

    class Meta:
        verbose_name = 'Unidad de Medida'
        verbose_name_plural = 'Unidades de Medida'

    def __str__(self):
        return self.description


class Products(BaseModel):
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
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    barcode = models.CharField(max_length=50, verbose_name="Codigo de Barra")
    historical = HistoricalRecords()
    quotation = models.IntegerField(default=0)

    # Cantidad minima

    @property
    def _history_user(self):  # Registra que usuario ha hecho el cambio
        return self.change_by

    @_history_user.setter
    def _history_user(self, value):
        self.change_by = value

    # Genera un codigo unico de 6 digitos para cada producto
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = '{:06}'.format(random.randint(0, 999999))
        super().save(*args, **kwargs)

    # Solicita la cotizacion del producto sin alterar la db
    @staticmethod
    def product_quote(self, product_id, amount_to_quote):
        product = Products.objects.get(id=product_id)
        if product.quotation >= amount_to_quote:
            product.quotation -= amount_to_quote
            price_quote = product.pride * amount_to_quote
            product.save()
        else:
            price_quote = None

        return price_quote

    class Meta:
        verbose_name = 'Productos'

    def __str__(self):
        return self.name


# Manejo de bienes y propiedades del negocio
class CategorySupplies(BaseModel):
    description = models.CharField(max_length=100)
    state = models.BooleanField('Estado', default=True)
    historical = HistoricalRecords()

    @property
    def _history_user(self):  # Registra que usuario ha hecho el cambio
        return self.change_by

    @_history_user.setter
    def _history_user(self, value):
        self.change_by = value

    class Meta:
        verbose_name = 'Categoria de Insumos'

    def __str__(self):
        return self.description


class Supplies(BaseModel):
    name = models.CharField(max_length=100)
    price = models.IntegerField('Precio del insumo')
    quantity = models.IntegerField('Cantidad del insumo')
    description = models.CharField(max_length=100)
    historical = HistoricalRecords()
    provider = models.ForeignKey(Providers, on_delete=models.CASCADE)
    category = models.ForeignKey(CategorySupplies, on_delete=models.CASCADE)
    state = models.BooleanField('Estado', default=True)

    @property
    def _history_user(self):  # Registra que usuario ha hecho el cambio
        return self.change_by

    @_history_user.setter
    def _history_user(self, value):
        self.change_by = value

    class Meta:
        verbose_name = 'Insumo'

    def __str__(self):
        return self.name


class CategoryAssets(BaseModel):
    description = models.CharField(max_length=100)
    state = models.BooleanField('Estado', default=True)
    historical = HistoricalRecords()

    @property
    def _history_user(self):  # Registra que usuario ha hecho el cambio
        return self.change_by

    @_history_user.setter
    def _history_user(self, value):
        self.change_by = value

    class Meta:
        verbose_name = 'Bienes y Propiedades'

    def __str__(self):
        return self.description


class Assets(BaseModel):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    date_of_purchase = models.DateField()
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(CategoryAssets, on_delete=models.CASCADE)
    site_operation = models.CharField(max_length=100)
    historical = HistoricalRecords()

    @property
    def _history_user(self):  # Registra que usuario ha hecho el cambio
        return self.change_by

    @_history_user.setter
    def _history_user(self, value):
        self.change_by = value

    class Meta:
        verbose_name = 'Biene y/o Activo'
        verbose_name_plural = 'Bienes y/o Activos'

    def __str__(self):
        return self.name
