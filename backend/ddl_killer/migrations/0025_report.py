from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ddl_killer', '0024_message_usermessage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('rid', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ddl_killer.User')),
            ],
        ),
    ]
