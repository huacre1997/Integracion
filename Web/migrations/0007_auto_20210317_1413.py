# Generated by Django 3.1.6 on 2021-03-17 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0006_auto_20210317_1359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posicionesllantas',
            name='posicion',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='posicionesllantas',
            name='posx',
            field=models.CharField(blank=True, default='0', max_length=20),
        ),
        migrations.AlterField(
            model_name='posicionesllantas',
            name='posy',
            field=models.CharField(blank=True, default='0', max_length=20),
        ),
    ]
