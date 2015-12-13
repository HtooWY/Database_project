'''
Created on Nov 27, 2015

@author: Wai Yan
'''


import MySQLdb as mdb
import datetime
if __name__ == '__main__':
#     user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
#     user.save()
    con=mdb.connect(host='localhost', user="htoowaiyan", passwd="Admin@12345",db="game_community")

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
#         cur.execute("insert into rate_game(playerid,gameid,gamescore) values(%s,%s,%s)"%(1,3,1))
#         cur.execute("select AVg(gamescore) from rate_game where gameid=3")
#         cur.execute("update game set score=(select AVg(gamescore) from rate_game where gameid=3) where gameid=3")
#         cur.execute("select * from game")
#         games=cur.fetchall()
# #         for game in games:
# #             print game[1]
#         print type(games)
#         cur.execute("insert into comments(commenterid,receiverid,comment_content,comment_time) values(%s,%s,'%s','%s')"%(3,3,"hi",datetime.datetime.now()))
#         cur.execute("select loginname, receiverid, comment_content from comments, player where player.playerid=comments.commenterid and receiverid=3")
#         cur.execute("select loginname, review from reviews,player where reviews.gameid=1 and reviews.playerid=player.playerid")
        cur.execute("select * from player where loginname like '%%%s%%'"%("ad"))
        print cur.fetchall()
#         cur.execute("insert into ordergame(playerid,gameid,numoforder) values (2,4,1)")
#         cur.execute("select title,SUM(numoforder) as total from game g, ordergame o where o.gameid=g.gameid group by title order by total desc")
        print "finish"
