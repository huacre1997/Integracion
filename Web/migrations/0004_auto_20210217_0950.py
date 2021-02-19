# Generated by Django 3.1.6 on 2021-02-17 14:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0003_auto_20210215_0930'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cubierta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('condicion', models.IntegerField(blank=True, choices=[(1, 'Nuevo'), (2, 'Reencauchado')], null=True)),
                ('nro_reencauchado', models.IntegerField(blank=True, null=True)),
                ('ancho_banda', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('altura_ini', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('altura_fin', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('altura', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('costo', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('km', models.DecimalField(decimal_places=2, max_digits=10)),
                ('modelo_banda', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Web.modelorenova')),
                ('renovadora', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Web.anchobandarenova')),
            ],
        ),
        migrations.AddField(
            model_name='llanta',
            name='cubierta',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Web.cubierta'),
        ),
    ]
