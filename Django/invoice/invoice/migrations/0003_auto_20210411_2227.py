# Generated by Django 3.1.7 on 2021-04-11 15:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0002_auto_20210406_0147'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoicedetail',
            name='invoice',
        ),
        migrations.AddField(
            model_name='invoice',
            name='invoice_detail',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='invoice.invoicedetail'),
        ),
    ]
