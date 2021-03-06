# Generated by Django 3.0.5 on 2020-05-29 06:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ddl_killer', '0023_securitykeypair'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('mid', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField(blank=True, null=True)),
                ('category', models.CharField(max_length=100)),
                ('publish_time', models.CharField(blank=True, max_length=50, null=True)),
                ('publisher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ddl_killer.User')),
            ],
        ),
        migrations.CreateModel(
            name='UserMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_read', models.BooleanField(default=False)),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ddl_killer.Message')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ddl_killer.User')),
            ],
        ),
    ]
