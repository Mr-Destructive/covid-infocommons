# Generated by Django 4.0.2 on 2022-12-20 17:31

from django.db import migrations, models
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0010_alter_person_websites'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='keywords',
            field=django_mysql.models.ListCharField(models.CharField(blank=True, max_length=1000, null=True), blank=True, max_length=1000, null=True, size=None),
        ),
    ]
