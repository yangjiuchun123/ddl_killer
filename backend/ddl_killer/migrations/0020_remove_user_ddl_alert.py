# Generated by Django 3.0.5 on 2020-05-22 19:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ddl_killer', '0019_user_ddl_alert'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='ddl_alert',
        ),
    ]