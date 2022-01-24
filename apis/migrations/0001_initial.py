# Generated by Django 3.2.8 on 2022-01-24 19:48

from django.db import migrations, models
import django.db.models.deletion
import django_mysql.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Funder',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('ror', models.CharField(blank=True, max_length=255, null=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'funder',
            },
        ),
        migrations.CreateModel(
            name='Grant',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('award_id', models.CharField(blank=True, max_length=255, null=True)),
                ('title', models.TextField(blank=True, null=True)),
                ('funder_divisions', django_mysql.models.ListCharField(models.CharField(blank=True, max_length=200, null=True), blank=True, default=list, max_length=100, size=None)),
                ('program_reference_codes', django_mysql.models.ListCharField(models.CharField(blank=True, max_length=200, null=True), blank=True, default=list, max_length=1000, size=None)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('award_amount', models.IntegerField(blank=True, null=True)),
                ('abstract', models.TextField(blank=True, null=True)),
                ('keywords', django_mysql.models.ListCharField(models.CharField(blank=True, max_length=255, null=True), blank=True, max_length=100, null=True, size=None)),
            ],
            options={
                'db_table': 'grant',
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('ror', models.CharField(blank=True, max_length=1000)),
                ('name', models.CharField(blank=True, max_length=1000)),
                ('address', models.TextField(blank=True)),
                ('city', models.CharField(blank=True, max_length=1000)),
                ('state', models.CharField(blank=True, max_length=1000)),
                ('zip', models.CharField(blank=True, max_length=1000)),
                ('country', models.CharField(blank=True, max_length=1000)),
            ],
            options={
                'db_table': 'organization',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('first_name', models.CharField(blank=True, max_length=1000, null=True)),
                ('last_name', models.CharField(blank=True, max_length=1000, null=True)),
                ('orcid', models.CharField(blank=True, max_length=1000, null=True)),
                ('emails', models.TextField(blank=True, null=True)),
                ('private_emails', models.CharField(blank=True, max_length=1000, null=True)),
                ('keywords', django_mysql.models.ListCharField(models.CharField(blank=True, max_length=1000, null=True), blank=True, max_length=100, null=True, size=None)),
                ('affiliations', models.ManyToManyField(blank=True, to='apis.Organization')),
            ],
            options={
                'db_table': 'person',
            },
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('doi', models.CharField(blank=True, max_length=255, null=True)),
                ('title', models.TextField(blank=True, null=True)),
                ('issn', models.CharField(blank=True, max_length=255, null=True)),
                ('keywords', django_mysql.models.ListCharField(models.CharField(blank=True, max_length=255, null=True), blank=True, max_length=100, null=True, size=None)),
                ('language', models.CharField(blank=True, max_length=255, null=True)),
                ('publication_date', models.DateField(blank=True, null=True)),
                ('publication_type', models.CharField(blank=True, max_length=255, null=True)),
                ('authors', models.ManyToManyField(blank=True, to='apis.Person')),
                ('grants', models.ManyToManyField(blank=True, to='apis.Grant')),
            ],
            options={
                'db_table': 'publication',
            },
        ),
        migrations.AddField(
            model_name='grant',
            name='awardee_organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='apis.organization'),
        ),
        migrations.AddField(
            model_name='grant',
            name='funder',
            field=models.ForeignKey(blank=True, db_column='funder', null=True, on_delete=django.db.models.deletion.CASCADE, to='apis.funder'),
        ),
        migrations.AddField(
            model_name='grant',
            name='other_investigators',
            field=models.ManyToManyField(blank=True, related_name='grant_other_investigators', to='apis.Person'),
        ),
        migrations.AddField(
            model_name='grant',
            name='principal_investigator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='grant_pi', to='apis.person'),
        ),
        migrations.AddField(
            model_name='grant',
            name='program_officials',
            field=models.ManyToManyField(blank=True, to='apis.Person'),
        ),
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('doi', models.CharField(blank=True, max_length=255, null=True)),
                ('title', models.TextField(blank=True, null=True)),
                ('download_path', models.CharField(blank=True, max_length=255, null=True)),
                ('size', models.CharField(blank=True, max_length=255, null=True)),
                ('mime_type', models.CharField(blank=True, max_length=255, null=True)),
                ('authors', models.ManyToManyField(blank=True, to='apis.Person')),
                ('grants', models.ManyToManyField(blank=True, to='apis.Grant')),
                ('publications', models.ManyToManyField(blank=True, to='apis.Publication')),
            ],
            options={
                'db_table': 'dataset',
            },
        ),
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('doi', models.CharField(blank=True, max_length=1000, null=True)),
                ('filename', models.CharField(blank=True, max_length=1000, null=True)),
                ('download_path', models.CharField(blank=True, max_length=1000, null=True)),
                ('size', models.CharField(blank=True, max_length=1000, null=True)),
                ('keywords', django_mysql.models.ListCharField(models.CharField(blank=True, max_length=1000, null=True), blank=True, max_length=100, null=True, size=None)),
                ('mime_type', models.CharField(blank=True, max_length=1000, null=True)),
                ('checksum', models.CharField(blank=True, max_length=1000, null=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='apis.person')),
                ('dataset', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='apis.dataset')),
                ('grant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='apis.grant')),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='apis.organization')),
                ('publication', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='apis.publication')),
            ],
            options={
                'db_table': 'asset',
            },
        ),
    ]
