# Generated by Django 3.1.3 on 2021-03-13 16:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0007_auto_20210313_1355'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seguidores',
            name='siguido',
        ),
        migrations.AddField(
            model_name='seguidores',
            name='seguido',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='Seguido', to='auth.user'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='seguidores',
            name='sigue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='Sigue', to=settings.AUTH_USER_MODEL),
        ),
    ]