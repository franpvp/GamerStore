# Generated by Django 4.2.5 on 2023-09-20 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='role',
            field=models.CharField(choices=[('admin', 'administrador'), ('cliente', 'Clientes')], max_length=20),
        ),
    ]
