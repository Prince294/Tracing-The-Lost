# Generated by Django 4.0.4 on 2022-12-11 18:22

from django.db import migrations, models
import finding_people.models


class Migration(migrations.Migration):

    dependencies = [
        ('finding_people', '0005_alter_trackinguserdata_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trackinguserdata',
            name='session',
        ),
        migrations.AlterField(
            model_name='trackinguserdata',
            name='profile',
            field=models.ImageField(default='None', upload_to=finding_people.models.PathAndRename('TrackingImage')),
        ),
    ]
