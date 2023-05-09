from django import forms
from django.db import models
from django.urls import reverse
from simple_history.models import HistoricalRecords
from base.models import BaseModel

# Create your models here.

SOCIAL_CHOICES = (
    ('NATURAL', 'Natural'),
    ('JURIDICA', 'Juridica'),
)


class Company(BaseModel):
    name = models.CharField(max_length=100)
    social_id = models.IntegerField(unique=True)
    phone = models.BigIntegerField()
    email = models.EmailField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    description = models.CharField(max_length=100)
    historical = HistoricalRecords()

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not str(phone).isdigit():
            raise forms.ValidationError('El teléfono debe ser un número entero.')
        return phone

    @property
    def _history_user(self):  # Registra que usuario ha hecho el cambio
        return self.change_by

    @_history_user.setter
    def _history_user(self, value):
        self.change_by = value

    class Meta:
        verbose_name = "Empresa y/o Compañia"

    def __str__(self):
        return self.name


# Especifica la lista de clientes siemples aparte de empresas
class SimpleClients(BaseModel):
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=30)
    dni = models.IntegerField(unique=True)
    social_id = models.CharField(unique=True, max_length=50, choices=SOCIAL_CHOICES)
    is_active = models.BooleanField(default=True)
    phone = models.IntegerField()
    email = models.EmailField()
    historical = HistoricalRecords

    @property
    def _history_user(self):  # Registra que usuario ha hecho el cambio
        return self.change_by

    @_history_user.setter
    def _history_user(self, value):
        self.change_by = value

    class Meta:
        verbose_name = "Cliente Simple"

    def __str__(self):
        return self.name


class Providers(BaseModel):
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    dni = models.IntegerField(unique=True)
    social_id = models.IntegerField(unique=True)
    is_active = models.BooleanField(default=True)
    phone = models.IntegerField()
    email = models.EmailField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    historical = HistoricalRecords

    @property
    def _history_user(self):  # Registra que usuario ha hecho el cambio
        return self.change_by

    @_history_user.setter
    def _history_user(self, value):
        self.change_by = value

    class Meta:
        verbose_name = "Proveedores"

    def __str__(self):
        return self.name


class SimpleProvider(BaseModel):
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    dni = models.IntegerField()
    social_id = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    phone = models.IntegerField()
    email = models.EmailField(blank=True, null=True)
    historical = HistoricalRecords

    @property
    def _history_user(self):  # Registra que usuario ha hecho el cambio
        return self.change_by

    @_history_user.setter
    def _history_user(self, value):
        self.change_by = value

    class Meta:
        verbose_name = "Proveedor Simple"

    def __str__(self):
        return self.name
