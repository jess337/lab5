# Generated by Django 5.1.4 on 2025-01-09 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('health_data_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicaldata',
            name='date',
            field=models.CharField(),
        ),
    ]
