# Generated by Django 3.1.7 on 2021-05-16 11:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0010_auto_20210514_1641'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='EstadoAbastecimiento',
            new_name='EstadoViaje',
        ),
        migrations.AddField(
            model_name='abastecimiento',
            name='estado_viaje',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.PROTECT, to='Web.estadoviaje'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicalabastecimiento',
            name='estado_viaje',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='Web.estadoviaje'),
        ),
    ]
