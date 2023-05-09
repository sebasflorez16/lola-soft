# Generated by Django 4.1 on 2023-04-19 14:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Company",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("state", models.BooleanField(default=True, verbose_name="Estado")),
                (
                    "created_date",
                    models.DateField(
                        auto_now_add=True, verbose_name="Fecha de Creación"
                    ),
                ),
                (
                    "modified_date",
                    models.DateField(
                        auto_now=True, verbose_name="Fecha de Modificacion"
                    ),
                ),
                (
                    "deleted_date",
                    models.DateField(
                        auto_now=True, verbose_name="Fecha de Eliminacion"
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("social_id", models.IntegerField(unique=True)),
                ("phone", models.BigIntegerField()),
                ("email", models.EmailField(blank=True, max_length=254, null=True)),
                ("is_active", models.BooleanField(default=True)),
                ("description", models.CharField(max_length=100)),
            ],
            options={
                "verbose_name": "Empresa y/o Compañia",
            },
        ),
        migrations.CreateModel(
            name="SimpleClients",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("state", models.BooleanField(default=True, verbose_name="Estado")),
                (
                    "created_date",
                    models.DateField(
                        auto_now_add=True, verbose_name="Fecha de Creación"
                    ),
                ),
                (
                    "modified_date",
                    models.DateField(
                        auto_now=True, verbose_name="Fecha de Modificacion"
                    ),
                ),
                (
                    "deleted_date",
                    models.DateField(
                        auto_now=True, verbose_name="Fecha de Eliminacion"
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("last_name", models.CharField(max_length=30)),
                ("dni", models.IntegerField(unique=True)),
                (
                    "social_id",
                    models.CharField(
                        choices=[("NATURAL", "Natural"), ("JURIDICA", "Juridica")],
                        max_length=50,
                        unique=True,
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("phone", models.IntegerField()),
                ("email", models.EmailField(max_length=254)),
            ],
            options={
                "verbose_name": "Cliente Simple",
            },
        ),
        migrations.CreateModel(
            name="SimpleProvider",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("state", models.BooleanField(default=True, verbose_name="Estado")),
                (
                    "created_date",
                    models.DateField(
                        auto_now_add=True, verbose_name="Fecha de Creación"
                    ),
                ),
                (
                    "modified_date",
                    models.DateField(
                        auto_now=True, verbose_name="Fecha de Modificacion"
                    ),
                ),
                (
                    "deleted_date",
                    models.DateField(
                        auto_now=True, verbose_name="Fecha de Eliminacion"
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("last_name", models.CharField(max_length=50)),
                ("dni", models.IntegerField()),
                ("social_id", models.IntegerField(blank=True, null=True)),
                ("is_active", models.BooleanField(default=True)),
                ("phone", models.IntegerField()),
                ("email", models.EmailField(blank=True, max_length=254, null=True)),
            ],
            options={
                "verbose_name": "Proveedor Simple",
            },
        ),
        migrations.CreateModel(
            name="Providers",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("state", models.BooleanField(default=True, verbose_name="Estado")),
                (
                    "created_date",
                    models.DateField(
                        auto_now_add=True, verbose_name="Fecha de Creación"
                    ),
                ),
                (
                    "modified_date",
                    models.DateField(
                        auto_now=True, verbose_name="Fecha de Modificacion"
                    ),
                ),
                (
                    "deleted_date",
                    models.DateField(
                        auto_now=True, verbose_name="Fecha de Eliminacion"
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("last_name", models.CharField(max_length=50)),
                ("dni", models.IntegerField(unique=True)),
                ("social_id", models.IntegerField(unique=True)),
                ("is_active", models.BooleanField(default=True)),
                ("phone", models.IntegerField()),
                ("email", models.EmailField(max_length=254)),
                (
                    "company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="directory.company",
                    ),
                ),
            ],
            options={
                "verbose_name": "Proveedores",
            },
        ),
        migrations.CreateModel(
            name="HistoricalCompany",
            fields=[
                ("id", models.IntegerField(blank=True, db_index=True)),
                ("state", models.BooleanField(default=True, verbose_name="Estado")),
                (
                    "created_date",
                    models.DateField(
                        blank=True, editable=False, verbose_name="Fecha de Creación"
                    ),
                ),
                (
                    "modified_date",
                    models.DateField(
                        blank=True, editable=False, verbose_name="Fecha de Modificacion"
                    ),
                ),
                (
                    "deleted_date",
                    models.DateField(
                        blank=True, editable=False, verbose_name="Fecha de Eliminacion"
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("social_id", models.IntegerField(db_index=True)),
                ("phone", models.BigIntegerField()),
                ("email", models.EmailField(blank=True, max_length=254, null=True)),
                ("is_active", models.BooleanField(default=True)),
                ("description", models.CharField(max_length=100)),
                ("history_id", models.AutoField(primary_key=True, serialize=False)),
                ("history_date", models.DateTimeField(db_index=True)),
                ("history_change_reason", models.CharField(max_length=100, null=True)),
                (
                    "history_type",
                    models.CharField(
                        choices=[("+", "Created"), ("~", "Changed"), ("-", "Deleted")],
                        max_length=1,
                    ),
                ),
                (
                    "history_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "historical Empresa y/o Compañia",
                "verbose_name_plural": "historical Empresa y/o Compañias",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": ("history_date", "history_id"),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
