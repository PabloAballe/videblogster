# Generated by Django 2.2.10 on 2020-10-27 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20201027_0909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='porfile',
            name='paypal',
            field=models.EmailField(default='', help_text='Tu cuenta de PayPal para recibir los pagos', max_length=254),
        ),
    ]
