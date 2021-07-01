# Generated by Django 3.2 on 2021-07-01 07:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.IntegerField(default=0)),
                ('Description', models.CharField(default='', max_length=150)),
                ('ProjectType', models.CharField(choices=[('Production Projects', 'Production Projects'), ('College Projects', 'College Projects'), ('Others', 'Others')], default='', max_length=40)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Developer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Skills', models.CharField(choices=[('Web Development', 'Web Development'), ('Android Development', 'Android Development'), ('Artificial Intelligence', 'Artificial Intelligence'), ('Machine Learning', 'Machine Learning'), ('Data Sceince', 'Data Science')], default='', max_length=40)),
                ('Description', models.CharField(default='', max_length=150)),
                ('mobile', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='userType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userType', models.CharField(choices=[('Developer', 'Developer'), ('Client', 'Client')], default='', max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(max_length=50)),
                ('Date', models.DateField(default=django.utils.timezone.now)),
                ('ActualPrice', models.IntegerField(blank=True, default=0)),
                ('CoderPrice', models.IntegerField(blank=True, default=0)),
                ('Description', models.CharField(default='', max_length=200)),
                ('Status', models.CharField(choices=[('Not Accepted', 'Not Accepted'), ('Accepted', 'Accepted'), ('Assigned', 'Assigned'), ('Delievred', 'Delievred'), ('Completed', 'Completed')], default='Not Accepted', max_length=40)),
                ('PaymentStatus', models.CharField(choices=[('Not Paid', 'Not Paid'), ('Partially Paid', 'Partially Paid'), ('Fully Paid', 'Fully Paid')], default='Not Paid', max_length=40)),
                ('projectType', models.CharField(choices=[('Dissertation', 'Dissertation'), ('Assignment', 'Assignment'), ('Technical Report', 'Technical Report'), ('Others', 'Others')], default='', max_length=30)),
                ('CompletePercentage', models.CharField(blank=True, choices=[('25%', '25%'), ('50%', '50%'), ('75%', '75%'), ('100%', '100%')], default=0, max_length=25)),
                ('SentTO', models.ManyToManyField(blank=True, to='app.Developer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.client')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Amount', models.IntegerField(default=0)),
                ('Date', models.DateField(default=django.utils.timezone.now)),
                ('projectName', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.project')),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('files', models.FileField(blank=True, upload_to='projects')),
                ('fileName', models.CharField(blank=True, max_length=100)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bidAmount', models.IntegerField(default=0)),
                ('projectName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.project')),
                ('userName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.developer')),
            ],
            options={
                'unique_together': {('userName', 'projectName')},
            },
        ),
        migrations.CreateModel(
            name='Assign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Amount', models.IntegerField(default=0)),
                ('Date', models.DateField(default=django.utils.timezone.now)),
                ('projectName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.project')),
                ('userName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.developer')),
            ],
            options={
                'unique_together': {('userName', 'projectName')},
            },
        ),
    ]
