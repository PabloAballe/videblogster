# Generated by Django 2.2.10 on 2020-09-15 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_delete_seguir'),
    ]

    operations = [
        migrations.AddField(
            model_name='porfile',
            name='cover',
            field=models.ImageField(default='default/porfile.png', upload_to='porfile/images'),
        ),
        migrations.AlterField(
            model_name='post',
            name='categoria',
            field=models.CharField(choices=[('hogar', 'HOGAR'), ('deportes', 'DEPORTES'), ('tecnologia', 'TECNOLOGIA'), ('ciencia', 'CIENCIA'), ('salud', 'SALUD'), ('estilodevida', 'ESTILO_DE_VIDA'), ('mundo', 'MUNDO'), ('utilidades', 'UTILIDADES'), ('cocina', 'COCINA'), ('tutoriales', 'TUTORIALES'), ('bloguer', 'BLOGUER'), ('cultura', 'CULTURA'), ('negocios', 'NEGOCIOS'), ('politica', 'POLITICA'), ('opinion', 'OPINION'), ('fashion', 'FASHION'), ('viajes', 'VIAJES')], default='bloguer', help_text='Categoria del artículo', max_length=20),
        ),
        migrations.AlterField(
            model_name='post',
            name='titulo',
            field=models.CharField(help_text='Título del artículo', max_length=100),
        ),
    ]
