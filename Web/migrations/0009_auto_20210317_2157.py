# Generated by Django 3.1.6 on 2021-03-17 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0008_auto_20210317_2142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posicionesllantas',
            name='posicion',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='posicionesllantas',
            name='posx',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='posicionesllantas',
            name='posy',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
