# Generated by Django 4.2.17 on 2025-02-26 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AddField(
            model_name='customuser',
            name='last_name',
            field=models.CharField(default='', max_length=30),
        ),
    ]
