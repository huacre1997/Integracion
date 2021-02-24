# Generated by Django 3.1.6 on 2021-02-23 16:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0023_remove_llanta_obs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='llanta',
            name='posicion',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='llanta',
            name='vehiculo',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='llantas', to='Web.vehiculo'),
        ),
    ]
