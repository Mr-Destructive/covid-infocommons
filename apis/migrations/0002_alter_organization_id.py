# Generated by Django 4.0.2 on 2022-02-15 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]