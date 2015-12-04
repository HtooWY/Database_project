# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('gameid', models.IntegerField(serialize=False, primary_key=True)),
                ('price', models.DecimalField(null=True, max_digits=10, decimal_places=2)),
                ('title', models.CharField(max_length=255, null=True, blank=True)),
                ('developer', models.CharField(max_length=255, null=True, blank=True)),
                ('release_date', models.DateField(null=True, blank=True)),
                ('score', models.DecimalField(null=True, max_digits=2, decimal_places=1, blank=True)),
                ('genre', models.CharField(max_length=30, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('playerid', models.IntegerField(serialize=False, primary_key=True)),
                ('loginname', models.CharField(max_length=35)),
                ('password', models.CharField(max_length=32, null=True, blank=True)),
                ('join_date', models.DateTimeField(null=True, blank=True)),
                ('score', models.DecimalField(null=True, max_digits=2, decimal_places=1, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Plays',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('play_status', models.CharField(max_length=13, null=True, blank=True)),
                ('gameid', models.ForeignKey(to='Game_store.Game', db_column=b'gameid')),
                ('playerid', models.ForeignKey(to='Game_store.Player', db_column=b'playerid')),
            ],
        ),
        migrations.CreateModel(
            name='RateGame',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gamescore', models.IntegerField(null=True, blank=True)),
                ('gameid', models.ForeignKey(to='Game_store.Game', db_column=b'gameid')),
                ('playerid', models.ForeignKey(to='Game_store.Player', db_column=b'playerid')),
            ],
        ),
        migrations.CreateModel(
            name='RateReview',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rating', models.SmallIntegerField(null=True, blank=True)),
                ('playerid', models.ForeignKey(to='Game_store.Player', db_column=b'playerid')),
            ],
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('reviewid', models.IntegerField(serialize=False, primary_key=True)),
                ('review', models.TextField(null=True, blank=True)),
                ('review_time', models.DateTimeField(null=True, blank=True)),
                ('rating', models.IntegerField(null=True, blank=True)),
                ('gameid', models.ForeignKey(db_column=b'gameid', blank=True, to='Game_store.Game', null=True)),
                ('playerid', models.ForeignKey(db_column=b'playerid', blank=True, to='Game_store.Player', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='ratereview',
            name='reviewid',
            field=models.ForeignKey(to='Game_store.Reviews', db_column=b'reviewid'),
        ),
        migrations.AlterUniqueTogether(
            name='ratereview',
            unique_together=set([('reviewid', 'playerid')]),
        ),
        migrations.AlterUniqueTogether(
            name='rategame',
            unique_together=set([('gameid', 'playerid')]),
        ),
        migrations.AlterUniqueTogether(
            name='plays',
            unique_together=set([('playerid', 'gameid')]),
        ),
    ]
