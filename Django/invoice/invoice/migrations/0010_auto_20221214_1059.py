# Generated by Django 3.1.7 on 2022-12-14 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0009_auto_20221214_1031'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='comments',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
