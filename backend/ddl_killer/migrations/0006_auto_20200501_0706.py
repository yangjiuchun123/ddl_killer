# Generated by Django 3.0.5 on 2020-05-01 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ddl_killer', '0005_resource'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=100),
        ),
    ]
