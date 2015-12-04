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
                 price decimal(10,2),\
                 title varchar(255),\
                 developer varchar(255),\
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
                     foreign key (playerid) references player(playerid)\
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
        cur.execute("create table challenges(challengerid integer AUTO_INCREMENT,\
                        accepterid integer,\
                        gameid integer,\
                        challengeid integer,\
                        cha_time datetime,\
                        outcome varchar(4) check (outcome='Win' or outcome='Lose' or outcome = 'Draw'),\
                        primary key (challengeid),\
                        foreign key (challengerid) references player(playerid),\
                        foreign key (accepterid) references player(playerid),\
                        foreign key (gameid) references game(gameid)\
);")
        cur.execute("create table comments(commenterid integer AUTO_INCREMENT,\
                      receiverid integer,\
                      comment_content text,\
                      comment_time datetime,\
                      primary key (commenterid, receiverid),\
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
                       foreign key (playerid) references player(playerid),\
                       foreign key (gameid) references game(gameid),\
                       primary key (orderid)\
);")
        print "finish"
