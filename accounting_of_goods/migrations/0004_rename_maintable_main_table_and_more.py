# Generated by Django 4.2.2 on 2023-06-29 05:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounting_of_goods', '0003_rename_main_maintable'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MainTable',
            new_name='Main_table',
        ),
        migrations.RenameField(
            model_name='main_table',
            old_name='id_main',
            new_name='id_main_table',
        ),
        migrations.AlterModelTable(
            name='main_table',
            table='main_table',
        ),
    ]
