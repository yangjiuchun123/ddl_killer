# Generated by Django 3.0.5 on 2020-05-05 21:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ddl_killer', '0010_courseresource'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resource',
            name='course',
        ),
        migrations.RemoveField(
            model_name='task',
            name='course',
        ),
        migrations.AddField(
            model_name='task',
            name='course_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.CreateModel(
            name='CourseTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ddl_killer.Course')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ddl_killer.Task')),
            ],
        ),
    ]
