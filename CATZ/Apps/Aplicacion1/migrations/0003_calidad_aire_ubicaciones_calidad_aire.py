# Generated by Django 4.2.5 on 2023-11-14 02:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Aplicacion1', '0002_direcciones_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='calidad_aire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('indice_aqi', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='ubicaciones',
            name='calidad_aire',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Aplicacion1.calidad_aire'),
        ),
    ]
