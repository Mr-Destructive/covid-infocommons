# Generated by Django 4.0.2 on 2022-05-03 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0004_alter_grant_other_investigators'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grant',
            name='other_investigators',
            field=models.ManyToManyField(blank=True, related_name='grant_other_investigators', to='apis.Person'),
        ),
    ]
