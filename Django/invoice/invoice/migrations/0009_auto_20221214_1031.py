# Generated by Django 3.1.7 on 2022-12-14 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0008_auto_20221214_1030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='contact',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='email',
            field=models.EmailField(blank=True, default='', max_length=254, null=True),
        ),
    ]
