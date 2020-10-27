# Generated by Django 2.2.10 on 2020-10-27 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20201027_1002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='porfile',
            name='cover',
            field=models.ImageField(default='default/cover.png', help_text='Sube tu cover', upload_to='porfile/images/cover'),
        ),
        migrations.AlterField(
            model_name='porfile',
            name='imagen_perfil',
            field=models.ImageField(default='default/porfile.png', help_text='Imágen de Perfil', upload_to='porfile/images'),
        ),
        migrations.AlterField(
            model_name='post',
            name='imagen_principal',
            field=models.ImageField(help_text='Imágen principal', upload_to='posts/images'),
        ),
    ]