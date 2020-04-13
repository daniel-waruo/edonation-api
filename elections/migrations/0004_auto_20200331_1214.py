# Generated by Django 3.0.4 on 2020-03-31 09:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('elections', '0003_election_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='election',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='elections', to=settings.AUTH_USER_MODEL),
        ),
    ]
