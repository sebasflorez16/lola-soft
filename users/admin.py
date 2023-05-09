from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

# Register your models here.

from .models import User


class UserHistoryAdmin(SimpleHistoryAdmin):
    list_display = ["id", "username", "is_staff", "is_superuser"]
    history_list_display = ["is_active"]
    search_fields = ["name", "username"]



admin.site.register(User, UserHistoryAdmin)