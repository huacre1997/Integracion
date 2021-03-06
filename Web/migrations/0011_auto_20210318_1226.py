# Generated by Django 3.1.6 on 2021-03-18 17:26

import Web.models
from django.db import migrations, models
import functools


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0010_auto_20210318_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='foto_nueva',
            field=models.FileField(blank=True, null=True, upload_to=functools.partial(Web.models._update_filename, *(), **{'path': 'fotos/'})),
        ),
        migrations.AlterField(
            model_name='posicionesllantas',
            name='posx',
            field=models.CharField(default='0', max_length=15),
        ),
        migrations.AlterField(
            model_name='posicionesllantas',
            name='posy',
            field=models.CharField(default='0', max_length=15),
        ),
        migrations.AlterField(
            model_name='tipovehiculo',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='vehiculo2/Y/'),
        ),
        migrations.AlterField(
            model_name='tipovehiculo',
            name='image2',
            field=models.ImageField(blank=True, null=True, upload_to='vehiculo2/X'),
        ),
    ]
