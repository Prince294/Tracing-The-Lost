# Generated by Django 4.0.4 on 2022-12-20 07:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finding_people', '0013_remove_policestationdata_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trackinguserdata',
            old_name='police_station_droped',
            new_name='police_station_id',
        ),
        migrations.AlterField(
            model_name='trackinguserdata',
            name='time_at_droped',
            field=models.TimeField(default=datetime.time(13, 0, 34, 782196)),
        ),
    ]