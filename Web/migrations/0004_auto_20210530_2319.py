# Generated by Django 3.1.7 on 2021-05-30 23:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0003_auto_20210519_1737'),
    ]

    operations = [
        migrations.AddField(
            model_name='abastecimiento',
            name='estacion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Web.estaciones'),
        ),
        migrations.AddField(
            model_name='historicalabastecimiento',
            name='estacion',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='Web.estaciones'),
        ),
        migrations.AddField(
            model_name='historicalviaje',
            name='fecha_fin',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='historicalviaje',
            name='rend_cargado',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='historicalviaje',
            name='rend_prom',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='historicalviaje',
            name='rend_vacio',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='viaje',
            name='fecha_fin',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='viaje',
            name='rend_cargado',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='viaje',
            name='rend_prom',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='viaje',
            name='rend_vacio',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='abastecimiento',
            name='estado_viaje',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Web.estadoviaje'),
        ),
        migrations.AlterField(
            model_name='abastecimiento',
            name='producto',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Web.producto'),
        ),
        migrations.AlterField(
            model_name='abastecimiento',
            name='tipo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Web.tipoabastecimiento'),
        ),
        migrations.AlterField(
            model_name='abastecimiento',
            name='tramo',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='estaciones',
            name='ruta',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Web.ruta'),
        ),
        migrations.AlterField(
            model_name='estaciones',
            name='ubicacion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Web.departamento'),
        ),
        migrations.AlterField(
            model_name='estacionproducto',
            name='estacion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Web.estaciones'),
        ),
        migrations.AlterField(
            model_name='estacionproducto',
            name='producto',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Web.producto'),
        ),
        migrations.AlterField(
            model_name='historicalabastecimiento',
            name='tramo',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='historicalestaciones',
            name='ubicacion',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='Web.departamento'),
        ),
        migrations.AlterField(
            model_name='historicalrendimiento',
            name='rend_cargado',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='historicalrendimiento',
            name='rend_vacio',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='rendimiento',
            name='rend_cargado',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='rendimiento',
            name='rend_vacio',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='tramo',
            name='ruta',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Web.ruta'),
        ),
        migrations.AlterField(
            model_name='viaje',
            name='ruta',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Web.ruta'),
        ),
    ]
