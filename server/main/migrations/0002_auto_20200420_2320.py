# Generated by Django 3.0.5 on 2020-04-21 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='interview',
            field=models.CharField(max_length=120),
        ),
    ]
