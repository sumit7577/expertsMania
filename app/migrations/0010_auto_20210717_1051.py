# Generated by Django 3.2 on 2021-07-17 05:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20210716_2043'),
    ]

    operations = [
        migrations.AddField(
            model_name='assign',
            name='DeveloperDeadline',
            field=models.DateField(blank=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='ClientDeadline',
            field=models.DateField(blank=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
