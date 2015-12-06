'''
Created on Dec 5, 2015

@author: Wai Yan
'''
import MySQLdb as mdb
import datetime
if __name__ == '__main__':
   
    con=mdb.connect(host='localhost', user="htoowaiyan", passwd="Admin@12345",db="game_community")
    with con:
        cur=con.cursor()
#         cur.execute("insert into game(title,developer,genre,release_date) values('jj','ubisoft','action','%s')"%(datetime.datetime.now()))
#         cur.execute("select * from game")
#         cur.execute("insert into player values(1,'admin','password','%s',1)"%(datetime.datetime.now()))
#         cur.execute("insert into player values(2,'test','password','%s',1)"%(datetime.datetime.now()))
#         cur.execute("select review from reviews order by rating;")
#         rows=cur.fetchall()
#         for i in range(len(rows)):
#             print rows[i][0]
        cur.execute("insert into challenges(challengerid, accepterid, gameid, challengeid, cha_time, outcome) values(2,1,1,1, '%s','Win')"%(datetime.datetime.now()))
    print "finish"