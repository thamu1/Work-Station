# Generated by Django 3.1.7 on 2021-09-12 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0005_auto_20210413_1240'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_is_delete',
            field=models.BooleanField(default=True),
        ),
    ]
