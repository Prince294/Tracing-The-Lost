# Generated by Django 4.0.4 on 2022-12-20 09:42

import datetime
from django.db import migrations, models
import finding_people.models


class Migration(migrations.Migration):

    dependencies = [
        ('finding_people', '0016_alter_trackinguserdata_time_at_droped'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trackinguserdata',
            name='time_at_droped',
            field=models.TimeField(default=datetime.time(15, 12, 0, 553608)),
        ),
        migrations.AlterField(
            model_name='trackinguserdata',
            name='user_profile',
            field=models.ImageField(upload_to=finding_people.models.PathAndRename('TrackingImage')),
        ),
    ]
