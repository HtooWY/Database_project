'''
Created on Nov 27, 2015

@author: Wai Yan
'''
from django.contrib.auth.models import User

import MySQLdb as mdb
import datetime
if __name__ == '__main__':
#     user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
#     user.save()
    con=mdb.connect(host='localhost', user="htoowaiyan", passwd="Admin@12345",db="game_community")
    user = User.objects.create_user('johncena', email='lennon@thebeatles.com', password='johnpassword')
    user.save()
    with con:
        cur=con.cursor()
        # 
#         cur.execute("Drop table rate_game;")
#         cur.execute("Drop table comments;")
#         cur.execute("Drop table ordergame;")
#         cur.execute("Drop table challenges;")
#         cur.execute("Drop table plays;")
#         cur.execute("Drop table rate_review;")
#         cur.execute("Drop table reviews;")
#         cur.execute("Drop table game;")
#         cur.execute("Drop table player;")
#         cur.execute("Insert into player('loginname','password','datetime',) values('Admin','password','%s', 11)"%(datetime.datetime.now()))
#         cur.execute("CREATE TRIGGER challenge_end\
#                     AFTER UPDATE ON challenges\
#                     For Each Row\
#                     Begin\
#                         DECLARE num_wins integer;\
#                         DECLARE num_tot integer;\
#                         SET num_wins = (SELECT COUNT(*) FROM challenges \
#                                     WHERE (challengerid=New.challengerid AND outcome='Win') \
#                                     OR (accepterid=New.challengerid AND outcome='Lose'));\
#                         SET num_tot = (SELECT COUNT(*) FROM challenges \
#                                     WHERE (challengerid=New.challengerid)) \
#                                     OR (accepterid=New.challengerid);\
#                         UPDATE player SET score=num_win/num_tot*10.0 WHERE playerid=New.challengerid;\
#                         SET num_wins = (SELECT COUNT(*) FROM challenges \
#                                     WHERE (challengerid=New.accepterid AND outcome='Win') \
#                                     OR (accepterid=New.accepterid AND outcome='Lose'));\
#                         SET num_tot = (SELECT COUNT(*) FROM challenges \
#                                     WHERE (challengerid=New.accepterid) \
#                                     OR (accepterid=New.accepterid));\
#                         UPDATE player SET score=num_win/num_tot*10.0 WHERE playerid=New.accepterid;    \
# End;")
        cur.execute("inset into ")
        print "finish"
