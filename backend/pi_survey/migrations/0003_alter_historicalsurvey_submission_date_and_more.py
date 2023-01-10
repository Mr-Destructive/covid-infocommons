# Generated by Django 4.0.2 on 2022-12-22 19:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pi_survey', '0002_alter_historicalsurvey_person_additional_comments_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalsurvey',
            name='submission_date',
            field=models.DateTimeField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='survey',
            name='submission_date',
            field=models.DateTimeField(default=datetime.date.today),
        ),
    ]
