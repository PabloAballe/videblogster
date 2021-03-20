# Generated by Django 3.1.3 on 2021-03-19 21:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0009_remove_porfile_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='imagen_url',
            field=models.CharField(blank=True, default='', help_text='URL de la imagen', max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='porfile',
            name='usuario',
            field=models.OneToOneField(help_text='Nombre de usuario', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]