from datetime import date
from dateutil.relativedelta import relativedelta
from django.db import models
from base.models import BaseModel
from simple_history.models import HistoricalRecords
from users.models import User


# Para el manejo de todo lo relacionado al staff lo aplicaremos desde los users

# Agregar departamentos para enlazar los cargos de los users


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Usuario')
    salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Salario')
    birth_date = models.DateField('Fecha de Nacimiento')
    date_admission = models.DateField('Fecha de Ingreso', null=True, blank=True, auto_now_add=True)
    historical = HistoricalRecords()

    @property
    def _history_user(self):  # Registra que usuario ha hecho el cambio
        return self.change_by

    @_history_user.setter
    def _history_user(self, value):
        self.change_by = value

    def age(self):
        today = date.today()
        age = relativedelta(today, self.birth_date)
        return age.years

    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'

    def __str__(self):
        return self.user.name


class Department(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nombre')
    description = models.TextField(verbose_name='Descripción')
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='managed_departments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    historical = HistoricalRecords()

    @property
    def _history_user(self):  # Registra que usuario ha hecho el cambio
        return self.change_by

    @_history_user.setter
    def _history_user(self, value):
        self.change_by = value

    class Meta:
        verbose_name = 'Departamento'

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nombre del Cargo')
    description = models.TextField(verbose_name='Descripción')
    requirements = models.TextField(verbose_name='Requerimientos')
    responsibilities = models.TextField('Responsabilidades', blank=True, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Salario')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='Depertamento')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    historical = HistoricalRecords()

    @property
    def _history_user(self):  # Registra que usuario ha hecho el cambio
        return self.change_by

    @_history_user.setter
    def _history_user(self, value):
        self.change_by = value

    class Meta:
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'

    def __str__(self):
        return self.name


class Deductions(BaseModel):
    name = models.CharField(max_length=50, verbose_name='Nombre')
    description = models.CharField(max_length=100, verbose_name='Descripción')
    amount = models.IntegerField(verbose_name='Valor de la deduccíon')
    historical = HistoricalRecords()

    @property
    def _history_user(self):  # Registra que usuario ha hecho el cambio
        return self.change_by

    @_history_user.setter
    def _history_user(self, value):
        self.change_by = value

    class Meta:
        verbose_name = 'Deducción'
        verbose_name_plural = 'Deducciones'

    def __str__(self):
        return self.name


class Payroll(BaseModel):
    employee = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Usuario y/o Empleado')
    pay_date = models.DateField(auto_now_add=True, verbose_name='Ultimo pago')
    gross_salary = models.IntegerField('Salario Bruto')
    deductions = models.ForeignKey(Deductions, on_delete=models.CASCADE, verbose_name='Deducciones')
    net_salary = models.IntegerField()
    historical = HistoricalRecords()

    @property
    def _history_user(self):  # Registra que usuario ha hecho el cambio
        return self.change_by

    @_history_user.setter
    def _history_user(self, value):
        self.change_by = value

    # Calcula el precio final luego de deduciones
    def final_pay(self, *args, **kwargs):
        self.net_salary = self.gross_salary - self.deductions
        super(Payroll, self).save(*args, **kwargs)

    def get_last_payroll(self):
        last_payroll = self.objects.order_by('-pay_date').first()
        if last_payroll:
            return last_payroll.pk
        else:
            return None

    class Meta:
        verbose_name = 'Nomina'
        verbose_name_plural = 'Nominas'

    def __str__(self):
        return self.employee


class Project(models.Model):
    title = models.CharField(max_length=255, verbose_name='Nombre')
    description = models.TextField(verbose_name='Descripción')
    image = models.ImageField(blank=True, null=True, verbose_name='Imagen')
    completed = models.BooleanField(default=False, verbose_name='Completado')
    manager = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Gerente')
    is_active = models.BooleanField(default=True, verbose_name='Estado')
    historical = HistoricalRecords()

    @property
    def _history_user(self):  # Registra que usuario ha hecho el cambio
        return self.change_by

    @_history_user.setter
    def _history_user(self, value):
        self.change_by = value

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'


class Task(models.Model):
    title = models.CharField(max_length=50, verbose_name='Nombre del Proyecto')
    description = models.TextField(verbose_name='Descripción General')
    image = models.ImageField(blank=True, null=True)
    assigned_to = models.ManyToManyField(User, verbose_name='Usuarios Asignados')
    is_active = models.BooleanField(default=False, verbose_name='Estado')
    start_date = models.DateField(auto_now_add=True, verbose_name='Fecha de Início')
    end_date = models.DateField(verbose_name='Fecha Limite', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    historical = HistoricalRecords()

    @property
    def _history_user(self):  # Registra que usuario ha hecho el cambio
        return self.change_by

    @_history_user.setter
    def _history_user(self, value):
        self.change_by = value

    def get_percentage_completed(self):
        if self.state:
            return 100
        total_tasks = self.project.tasks.all().count()
        completed_tasks = self.project.tasks.filter(status=True).count()
        if total_tasks > 0:
            return round(completed_tasks / total_tasks * 100, 2)
        else:
            return 0

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Tarea'
        verbose_name_plural = 'Tareas'
