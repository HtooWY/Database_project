from django.db import models
from jsonschema._validators import maxLength

# Create your models here.
class Game(models.Model):
    gameid = models.IntegerField(primary_key=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    developer = models.CharField(max_length=255, blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    score = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    genre = models.CharField(max_length=30, blank=True, null=True)


class Player(models.Model):
    playerid = models.IntegerField(primary_key=True)
    loginname=models.CharField(max_length=35, blank=False)
    password = models.CharField(max_length=32, blank=True, null=True)
    join_date = models.DateTimeField(blank=True, null=True)
    score = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)


class Plays(models.Model):
    playerid = models.ForeignKey(Player, db_column='playerid')
    gameid = models.ForeignKey(Game, db_column='gameid')
    play_status = models.CharField(max_length=13, blank=True, null=True)

    class Meta:
        unique_together = (('playerid', 'gameid'),)


class RateGame(models.Model):
    playerid = models.ForeignKey(Player, db_column='playerid')
    gamescore = models.IntegerField(blank=True, null=True)
    gameid = models.ForeignKey(Game, db_column='gameid')

    class Meta:
        unique_together = (('gameid', 'playerid'),)


class RateReview(models.Model):
    reviewid = models.ForeignKey('Reviews', db_column='reviewid')
    playerid = models.ForeignKey(Player, db_column='playerid')
    rating = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        unique_together = (('reviewid', 'playerid'),)


class Reviews(models.Model):
    reviewid = models.IntegerField(primary_key=True)
    playerid = models.ForeignKey(Player, db_column='playerid', blank=True, null=True)
    review = models.TextField(blank=True, null=True)
    review_time = models.DateTimeField(blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)
    gameid = models.ForeignKey(Game, db_column='gameid', blank=True, null=True)
#     
# class Challenges(models.Model):
#     challengerid = models.ForeignKey('Player', db_column='playerid', related_name='challengerid', blank=True, null=True)
#     accepterid = models.ForeignKey('Player', db_column='playerid',related_name='accepterid', blank=True, null=True)
#     gameid = models.ForeignKey('Game', db_column='gameid', blank=True, null=True)
#     challengeid = models.IntegerField(primary_key=True)
#     cha_time = models.DateTimeField(blank=True, null=True)
#     outcome = models.CharField(max_length=4, blank=True, null=True)
# 
# class Comments(models.Model):
#     commenterid = models.ForeignKey('Player', db_column='playerid',related_name='commenterid',)
#     receiverid = models.ForeignKey('Player', db_column='playerid',related_name='receiverid',)
#     comment_content = models.TextField(blank=True, null=True)
#     comment_time = models.DateTimeField(blank=True, null=True)
# 
#     class Meta:
#         unique_together = (('commenterid', 'receiverid'),)
    

