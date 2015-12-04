'''
Created on Nov 27, 2015

@author: Wai Yan
'''
import MySQLdb as mdb
from django.contrib.auth.models import User
import datetime
if __name__ == '__main__':
    user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    user.save()
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
        print "finish"
