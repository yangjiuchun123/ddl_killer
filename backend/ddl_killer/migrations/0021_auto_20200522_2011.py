# Generated by Django 3.0.5 on 2020-05-22 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ddl_killer', '0020_remove_user_ddl_alert'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='participate_alert',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='resource_alert',
            field=models.BooleanField(default=False),
        ),
    ]
