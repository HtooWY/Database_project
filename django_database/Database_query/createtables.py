'''
Created on Nov 27, 2015

@author: Wai Yan
'''
import MySQLdb as mdb
if __name__ == '__main__':
   
    con=mdb.connect(host='localhost', user="htoowaiyan", passwd="Admin@12345",db="game_community")
    with con:
        cur=con.cursor()
        cur.execute("create table player(playerid int AUTO_INCREMENT,\
                   loginname char(35) NOT NULL Unique,\
                   password char(32),\
                   join_date datetime,\
                   score decimal(2,1),\
                   Check (score<=10 and score >=0),\
                   primary key (playerid)\
);")
        cur.execute("create table game(gameid integer AUTO_INCREMENT,\
                 title varchar(255),\
                 developer varchar(255),\
                 price decimal(10,2),\
                 release_date date,\
                 score decimal(2,1) check (score<=10 and score>=0),\
                 genre varchar(30),\
                 primary key (gameid)\
);")
        cur.execute("create table reviews(reviewid integer AUTO_INCREMENT,\
                     playerid integer,\
                     review text,\
                     review_time datetime,\
                     rating integer,\
                     gameid integer,\
                     primary key(reviewid),\
                     foreign key (gameid) references game(gameid),\
                     foreign key (playerid) references player(playerid),\
                     constraint pgid unique (gameid,playerid)\
);")
        cur.execute("create table rate_review(reviewid integer,\
                         playerid integer,\
                         rating smallint check (rating=-1 or rating=1),\
                         primary key (reviewid, playerid),\
                         foreign key (reviewid) references reviews(reviewid),\
                         foreign key (playerid) references player(playerid)\
);")
        cur.execute("create table plays(playerid integer,\
                   gameid integer,\
                   play_status varchar(13),\
                   Check (play_status='has played' or play_status='is playing' or play_status='wants to play'),\
                   primary key (playerid, gameid),\
                   foreign key (playerid) references player(playerid),\
                   foreign key (gameid) references game(gameid)\
);")
        cur.execute("create table challenges(challengerid integer,\
                        accepterid integer,\
                        gameid integer,\
                        challengeid integer AUTO_INCREMENT,\
                        cha_time datetime,\
                        outcome varchar(10) check (outcome='accepted' or outcome='declined' or outcome = 'canceled' or outcome='pending'),\
                        primary key (challengeid),\
                        foreign key (challengerid) references player(playerid),\
                        foreign key (accepterid) references player(playerid),\
                        foreign key (gameid) references game(gameid),\
                        constraint check_id CHECK (challengerid<>accepterid)\
);")
        cur.execute("create table comments(commenterid integer,\
                      receiverid integer,\
                      comment_content text,\
                      comment_time datetime,\
                      foreign key (commenterid) references player(playerid),\
                      foreign key (receiverid) references player(playerid)\
);")
        cur.execute("create table rate_game(playerid integer,\
                       gamescore integer check (gamescore<=10 and gamescore>=0),\
                       gameid integer,\
                       foreign key (playerid) references player(playerid),\
                       foreign key (gameid) references game(gameid),\
                       primary key (gameid, playerid)\
);")
        cur.execute("create table ordergame(orderid integer AUTO_INCREMENT,\
                       playerid integer,\
                       gameid integer,\
                       numoforder integer,\
                       order_time datetime,\
                       foreign key (playerid) references player(playerid),\
                       foreign key (gameid) references game(gameid),\
                       primary key (orderid)\
);")
        cur.execute("CREATE TRIGGER challenge_end\
                    AFTER UPDATE ON challenges\
                    For Each Row\
                    Begin\
                        DECLARE num_wins integer;\
                        DECLARE num_tot integer;\
                        SET num_wins = (SELECT COUNT(*) FROM challenges \
                                    WHERE (challengerid=New.challengerid AND outcome='Win') \
                                    OR (accepterid=New.challengerid AND outcome='Lose'));\
                        SET num_tot = (SELECT COUNT(*) FROM challenges \
                                    WHERE (challengerid=New.challengerid)) \
                                    OR (accepterid=New.challengerid);\
                        UPDATE player SET score=num_win/num_tot*10.0 WHERE playerid=New.challengerid;\
                        SET num_wins = (SELECT COUNT(*) FROM challenges \
                                    WHERE (challengerid=New.accepterid AND outcome='Win') \
                                    OR (accepterid=New.accepterid AND outcome='Lose'));\
                        SET num_tot = (SELECT COUNT(*) FROM challenges \
                                    WHERE (challengerid=New.accepterid) \
                                    OR (accepterid=New.accepterid));\
                        UPDATE player SET score=num_win/num_tot*10.0 WHERE playerid=New.accepterid;    \
End;")
        print "finish"
