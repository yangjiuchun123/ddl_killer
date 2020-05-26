from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ddl_killer', '0021_auto_20200522_2011'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='ddl_alert',
            field=models.BooleanField(default=True),
        ),
    ]
