# Generated by Django 3.2.8 on 2021-11-11 13:32

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_auth_expires'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='auth_expires',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 12, 13, 32, 12, 423798, tzinfo=utc)),
        ),
    ]
