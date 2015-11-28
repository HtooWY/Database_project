# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='course',
            fields=[
                ('cid', models.CharField(max_length=9, serialize=False, primary_key=True)),
                ('cname', models.CharField(max_length=60)),
                ('credits', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='faculty',
            fields=[
                ('fid', models.CharField(max_length=9, serialize=False, primary_key=True)),
                ('fname', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='teach',
            fields=[
                ('tid', models.CharField(max_length=9, serialize=False, primary_key=True)),
                ('semester', models.CharField(max_length=6)),
                ('year', models.IntegerField()),
                ('enrollment', models.IntegerField()),
                ('capacity', models.IntegerField()),
                ('cid', models.ForeignKey(to='app1.course', db_column=b'cid')),
                ('fid', models.ForeignKey(to='app1.faculty', db_column=b'fid')),
            ],
        ),
    ]
