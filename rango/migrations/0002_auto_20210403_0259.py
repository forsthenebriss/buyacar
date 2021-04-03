# Generated by Django 2.2.17 on 2021-04-03 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='is_new',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='slug',
            field=models.SlugField(null=True, unique=True),
        ),
    ]