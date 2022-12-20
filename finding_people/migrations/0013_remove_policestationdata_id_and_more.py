# Generated by Django 4.0.4 on 2022-12-20 07:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finding_people', '0012_policestationdata_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='policestationdata',
            name='id',
        ),
        migrations.RemoveField(
            model_name='policestationdata',
            name='stationid',
        ),
        migrations.AddField(
            model_name='policestationdata',
            name='station_id',
            field=models.AutoField(default=None, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='trackinguserdata',
            name='time_at_droped',
            field=models.TimeField(default=datetime.time(12, 52, 30, 752595)),
        ),
    ]
