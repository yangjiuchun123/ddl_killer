# Generated by Django 3.0.5 on 2020-06-05 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ddl_killer', '0026_merge_20200602_1809'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='repeat',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]