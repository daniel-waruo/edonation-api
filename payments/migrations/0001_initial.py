# Generated by Django 3.1.1 on 2020-10-05 09:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CampaignFeeTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.TextField(null=True, unique=True)),
                ('mpesa_code', models.CharField(max_length=200, null=True, unique=True)),
                ('phone', models.CharField(max_length=30)),
                ('reason_failed', models.TextField(null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=9)),
                ('transaction_cost', models.DecimalField(decimal_places=2, max_digits=9, null=True)),
                ('transaction_date', models.DateTimeField(auto_now=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('state', models.CharField(choices=[('requested', 'Payment Requested'), ('pending', 'Pending'), ('failed', 'Failed'), ('success', 'Success')], default='requested', max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='campaign_fee_transactions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
