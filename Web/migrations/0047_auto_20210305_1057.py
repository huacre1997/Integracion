# Generated by Django 3.1.6 on 2021-03-05 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0046_auto_20210305_1025'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vehiculo',
            name='nro_llantas',
        ),
        migrations.AddField(
            model_name='tipovehiculo',
            name='nro_llantas',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
