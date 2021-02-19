# Generated by Django 3.1.6 on 2021-02-18 01:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0005_cubierta_fech'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='llanta',
            name='cubierta',
        ),
        migrations.AddField(
            model_name='llanta',
            name='acciones',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='llanta',
            name='marca_llanta',
            field=models.ForeignKey(blank=True, default=True, on_delete=django.db.models.deletion.CASCADE, to='Web.marcallanta'),
        ),
        migrations.AddField(
            model_name='llanta',
            name='posicion',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='llanta',
            name='serie',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='llanta',
            name='unidad',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='llanta',
            name='almacen',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='Web.almacen'),
        ),
        migrations.AlterField(
            model_name='llanta',
            name='modelo_llanta',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='Web.modelollanta'),
        ),
        migrations.AlterField(
            model_name='llanta',
            name='ubicacion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='Web.ubicacion'),
        ),
        migrations.AlterField(
            model_name='llanta',
            name='vehiculo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='llantas', to='Web.vehiculo'),
        ),
        migrations.DeleteModel(
            name='Cubierta',
        ),
    ]
