from django.db import models
from django_tenants.models import TenantMixin, DomainMixin
import uuid


# Create your models here.


class Client(TenantMixin):
    name = models.CharField(max_length=100)
    paid_until = models.DateField()
    on_trial = models.BooleanField()
    created_on = models.DateField(auto_now_add=True)
    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)  # Universal Unique Identifiquer


class Domain(DomainMixin):
    pass


class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    state = models.BooleanField('Estado', default=True)
    created_date = models.DateField('Fecha de Creación', auto_now=False, auto_now_add=True)
    modified_date = models.DateField('Fecha de Modificacion', auto_now=True, auto_now_add=False)
    deleted_date = models.DateField('Fecha de Eliminacion', auto_now=True, auto_now_add=False)

    class Meta:
        abstract = True
        verbose_name = 'Modelo Base'
        verbose_name_plural = 'Modelos Bases'

    def __str__(self):
        pass
