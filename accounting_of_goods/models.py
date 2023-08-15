# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Category(models.Model):
    id_category = models.AutoField(primary_key=True)
    name = models.CharField('Category_name', max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'category'


class Division(models.Model):
    id_division = models.AutoField(primary_key=True)
    name = models.CharField('Division_name', max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'division'


class Main_table(models.Model):
    id_main = models.AutoField(primary_key=True)
    category = models.ForeignKey('Category', models.DO_NOTHING)
    product = models.ForeignKey('Product', models.DO_NOTHING)
    count = models.IntegerField('Count')
    operation = models.ForeignKey('Operation', models.DO_NOTHING)
    division = models.ForeignKey('Division', models.DO_NOTHING)
    date = models.DateTimeField('Date')

    def __str__(self):
        return f'{self.category.name} | "{self.product.name}", {self.operation.type_operation} {self.count}шт. за ({self.date}) '

    class Meta:
        managed = True
        db_table = 'main_table'


class Operation(models.Model):
    id_operation = models.TextField(primary_key=True)  # This field type is a guess.
    type_operation = models.CharField('Operation', max_length=10)

    def __str__(self):
        return self.type_operation

    class Meta:
        managed = True
        db_table = 'operation'


class Product(models.Model):
    id_product = models.AutoField(primary_key=True)
    name = models.CharField('Product_name',max_length=250)
    name_lower = models.CharField('Product_name_lower',max_length=250, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.name_lower = self.name.lower() if self.name else None
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'product'
