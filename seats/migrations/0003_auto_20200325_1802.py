# Generated by Django 3.0.4 on 2020-03-25 15:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('elections', '0002_auto_20200325_1802'),
        ('seats', '0002_seat_election'),
    ]

    operations = [
        migrations.AddField(
            model_name='seat',
            name='slug',
            field=models.SlugField(editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='seat',
            name='election',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='seats', to='elections.Election'),
        ),
        migrations.AlterUniqueTogether(
            name='seat',
            unique_together={('election', 'name'), ('election', 'slug')},
        ),
    ]
