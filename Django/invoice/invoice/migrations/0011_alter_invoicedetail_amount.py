# Generated by Django 4.2.3 on 2024-01-02 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0010_auto_20221214_1059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoicedetail',
            name='amount',
            field=models.IntegerField(default=1),
        ),
    ]
