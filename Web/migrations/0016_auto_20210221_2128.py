# Generated by Django 3.1.6 on 2021-02-22 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0015_auto_20210221_2125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medidallanta',
            name='medida',
            field=models.CharField(max_length=50),
        ),
    ]
