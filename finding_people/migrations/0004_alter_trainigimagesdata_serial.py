# Generated by Django 4.0.4 on 2022-12-11 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finding_people', '0003_alter_trainigimagesdata_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainigimagesdata',
            name='serial',
            field=models.IntegerField(),
        ),
    ]
