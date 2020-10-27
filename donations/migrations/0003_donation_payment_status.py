# Generated by Django 3.1.1 on 2020-10-27 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0002_auto_20201020_1319'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='payment_status',
            field=models.CharField(choices=[('pending', 'Pending'), ('failed', 'Failed'), ('success', 'Success')], default='pending', max_length=7),
        ),
    ]
