# Generated by Django 3.1.6 on 2021-02-08 23:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0002_investment_stock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investment',
            name='acquired_date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='investment',
            name='recent_date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]
