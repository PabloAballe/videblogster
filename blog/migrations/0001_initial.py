# Generated by Django 2.2.10 on 2020-09-09 07:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Porfile',
            fields=[
                ('id_porfile', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('imagen_perfil', models.ImageField(default='default/porfile.png', upload_to='porfile/images')),
                ('bio', models.CharField(blank=True, help_text='Escriba aqui su biografia', max_length=300, null=True)),
                ('vistas', models.IntegerField(default=0)),
                ('website', models.CharField(blank=True, default='', help_text='Ingresa tu sitio web', max_length=100, null=True)),
                ('email', models.EmailField(blank=True, default='', help_text='Tu Email', max_length=300, null=True)),
                ('seguidor', models.ManyToManyField(related_name='seguidor', to=settings.AUTH_USER_MODEL)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Porfiles',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id_post', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('titulo', models.CharField(help_text='Título del artículo', max_length=50)),
                ('descripcion', models.CharField(blank=True, default='', help_text='Descripción corta del artículo', max_length=300, null=True)),
                ('articulo', models.TextField(help_text='Escriba aquí su artículo')),
                ('imagen_principal', models.ImageField(upload_to='posts/images')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('publicado', models.BooleanField(default=False)),
                ('categoria', models.CharField(help_text='Categoria del artículo', max_length=50)),
                ('visitas', models.IntegerField(default=0)),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Porfile')),
            ],
            options={
                'verbose_name_plural': 'Posts',
            },
        ),
        migrations.CreateModel(
            name='PostGuardado',
            fields=[
                ('id_post_guardado', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('guardado_el', models.DateTimeField(default=django.utils.timezone.now)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Post')),
                ('usuario', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'PostGuardados',
            },
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id_post', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('comentario', models.TextField(help_text='Escriba aquí su comentario')),
                ('publicado', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('author_comentario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Porfile')),
                ('post_comentario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Post')),
            ],
            options={
                'verbose_name_plural': 'Comentarios',
            },
        ),
    ]