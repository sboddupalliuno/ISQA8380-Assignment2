# Generated by Django 3.1.6 on 2021-02-10 03:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0003_auto_20210208_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investment',
            name='recent_date',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]
