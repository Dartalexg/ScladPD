from django.contrib import admin
from .models import Category, Division, Main_table, Operation, Product

admin.site.register((Category, Division, Main_table, Operation, Product))



# Register your models here.
