# Generated by Django 4.1 on 2023-04-24 22:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("branches", "0002_remove_branch_users_alter_branch_manager"),
    ]

    operations = [
        migrations.AlterField(
            model_name="branch",
            name="manager",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
