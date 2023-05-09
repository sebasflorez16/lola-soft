from django.contrib import admin

# Register your models here.

from .models import *


admin.site.register(SubCategory)
admin.site.register(Category)
admin.site.register(Indicator)
admin.site.register(MeasureUnite)
admin.site.register(Products)
admin.site.register(CategorySupplies)
admin.site.register(Supplies)
admin.site.register(CategoryAssets)
admin.site.register(Assets)
