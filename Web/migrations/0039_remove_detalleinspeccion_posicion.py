# Generated by Django 3.1.6 on 2021-03-03 22:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0038_auto_20210303_1707'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detalleinspeccion',
            name='posicion',
        ),
    ]
