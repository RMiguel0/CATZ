# Generated by Django 4.2.5 on 2023-11-14 03:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Aplicacion1', '0003_calidad_aire_ubicaciones_calidad_aire'),
    ]

    operations = [
        migrations.AddField(
            model_name='calidad_aire',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
