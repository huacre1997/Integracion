# Generated by Django 3.1.6 on 2021-03-04 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0043_detalleinspeccion_repuesto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehiculo',
            name='ubicacion',
            field=models.CharField(blank=True, default='', max_length=50),
            preserve_default=False,
        ),
    ]
