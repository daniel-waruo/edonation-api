# Generated by Django 3.1.1 on 2020-10-02 10:46

from django.db import migrations
import pyuploadcare.dj.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20200922_1553'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=pyuploadcare.dj.models.ImageField(null=True),
        ),
    ]