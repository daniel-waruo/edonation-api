# Generated by Django 3.2.5 on 2021-08-02 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='amount_paid',
            field=models.DecimalField(decimal_places=2, max_digits=14, null=True),
        ),
        migrations.AddField(
            model_name='donationproduct',
            name='product_price',
            field=models.DecimalField(decimal_places=2, max_digits=14, null=True),
        ),
    ]