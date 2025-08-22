from django.contrib import admin
from .models import Product, Category
# Register your models here.

class AdminModel(admin.ModelAdmin):
    list_display = ('name', 'price', 'qty')

class CatAdminModel(admin.ModelAdmin):
    list_display = ('name', 'desc')

admin.site.register(Category, CatAdminModel)
admin.site.register(Product, AdminModel)