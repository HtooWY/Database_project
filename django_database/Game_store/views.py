from django.shortcuts import render,render_to_response,redirect
from django.http import HttpResponse,Http404,HttpRequest
from django.template.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext
import MySQLdb as mdb
import datetime
import MySQLdb
from django.contrib.redirects.models import Redirect

# Create your views here.

# Registration
def register(request):
    c = {}
    c.update(csrf(request))
    if "loginname" in request.POST:

        loginname=request.POST["loginname"]
        if loginname=="":
            c["norequest"]=True
            return render_to_response("register",c)
        password=request.POST["password"]
        email=request.POST["email"]
       
        conn=mdb.connect(host='localhost',user='htoowaiyan', passwd='Admin@12345',db='game_community')
        with conn:
            cursor=conn.cursor()
            try:
                cursor.execute("insert into player(loginname,password,join_date) values('%s','%s','%s')"%(loginname,password,datetime.datetime.now()))
                if email=="":
                    user = User.objects.create_user(loginname, password=password)
                else:
                    user = User.objects.create_user(loginname, email=email, password=password)
                user.save()
                
            except MySQLdb.IntegrityError as e:
                cursor.execute("Select * from player;")
                row=cursor.rowcount
                cursor.execute("ALTER TABLE player AUTO_INCREMENT=%s"%(str(row)))
                c["duplicate"]=True
                return render_to_response("register.html",c)
      
        return redirect("/login")
    else:
        
        return render(request,'register.html',c)

# Login
def login(request):
    c = {}
    c.update(csrf(request))
    if "loginname" in request.POST:
        username=request.POST["loginname"]
        password=request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            try:
                auth_login(request,user)
            except TypeError:
                c["notfound"]=True
                return render(request,'login.html',c)
            
            return redirect("/player/")
        
        return render(request,'login.html',c)
    else:
        return render(request,'login.html',c)
        
# Ordering new game
@login_required(login_url='/login/')
def orderGame(request,gid):
    conn=mdb.connect(host='localhost',user='htoowaiyan', passwd='Admin@12345',db='game_community')
    c={}
    c.update(csrf(request))
    c["gid"]=gid
    with conn:
        cursor=conn.cursor()
        cursor.execute("select playerid from player where loginname= '%s'"%(request.user.username))
        pid=cursor.fetchone()[0]
        cursor.execute("insert into ordergame(playerid,gameid,numoforder,order_time) values(%s,%s,1,'%s')"%(pid,gid,datetime.datetime.now()))
        cursor.execute("select orderid from ordergame order by orderid desc limit 1")
        oid=cursor.fetchone()[0]
        cursor.execute("select g.* from ordergame o1,ordergame o2, game g where o1.orderid=%s and o2.gameid=g.gameid and o1.gameid<>o2.gameid group by o2.gameid order by SUM(o2.numoforder)"%(oid))
        recomgames=cursor.fetchall()
#     if 'gameid' in request.POST:
#         gameid=request.POST['gameid']
#         if gameid=="":
#             
#             norequest=True
#             c["norequest"]=norequest
#             return render_to_response('ordernewgame.html',c)
#         else:
#             with conn:
#                 cursor=conn.cursor()
#                 cursor.execute("select playerid from player where loginname= '%s'"%(request.user.username))
#                 pid=cursor.fetchone()[0]
#                 cursor.execute("insert into ordergame(playerid,gameid,numoforder) values(%s,%s,1)"%(pid,gameid))
#                 if cursor.rowcount==0:
#                     raise Http404("Player not found")
#                 else:
#                     row = cursor.fetchone()
#                 return render_to_response('added.html',c)
#     
#     else:
#         return render_to_response('ordernewgame.html',c)
    c["gamelist"]=recomgames
    return render_to_response('buy_confirm.html',c)

# Add new game
@login_required(login_url='/login/')
def addNewGame(request):
    username=request.user.username
    conn=mdb.connect(host='localhost',user='htoowaiyan', passwd='Admin@12345',db='game_community')
    if username != "Admin":
        return render_to_response("notallowed.html")
    c = {}
    c.update(csrf(request))
    
    if 'title' in request.POST:
        title=request.POST['title']
        developer=request.POST['developer']
        Genre=request.POST['genre']
        
        if title=="":
            
            c["notitle"]=True
            return render_to_response('addnewgame.html',c)
        with conn:
            cursor=conn.cursor()
            cursor.execute("insert into game(title,developer,genre) values('%s','%s','%s')"%(title,developer,Genre))
            cursor.execute("select gameid from game where title='%s'"%(title))
            return redirect("/game/%s"%(cursor.fetchone()[0]))
    
    else:
        return render_to_response('addnewgame.html',c)


def index(request):
    c={}
    conn=mdb.connect(host='localhost',user='htoowaiyan', passwd='Admin@12345',db='game_community')
    with conn:
        cursor=conn.cursor()
        cursor.execute("select title,o.gameid,SUM(numoforder) as total from game g, ordergame o where o.gameid=g.gameid group by title order by total desc")
        gamelist=cursor.fetchall()
#     if request.user is not None:
#         c["login"]=True
#         return render_to_response("index.html",c)
    c["gamelist"]=gamelist
    return render_to_response("index.html",c)

# Search player 
def searchPlayer(request):
    c={}
    conn=mdb.connect(host='localhost',user='htoowaiyan', passwd='Admin@12345',db='game_community')
    if "loginname" in request.GET:        
        with conn:
            loginname=request.GET["loginname"]
            cursor=conn.cursor()
            cursor.execute("select * from player where loginname like '%%%s%%'"%(loginname))
            userlist=cursor.fetchall()
            c["userlist"]=userlist
#         if cursor.rowcount==0:
#             raise Http404("Player not found")
#         else:
#             row = cursor.fetchone()
#             context={'pid':row[0]}
#     if "submit" in request.GET:
#         if request.GET["submit"]=="get":
#             return redirect('/player/%s'%(row[0]))      
    return render(request,'searchplayer.html',c)



# User Record
def getUserRecord(request, pid):
    c={}
    conn=mdb.connect(host='localhost',user='htoowaiyan', passwd='Admin@12345',db='game_community')
    with conn:
        cursor=conn.cursor()
        
        cursor.execute("select * from player where loginname='%s'"%(request.user.username))
        playerid=cursor.fetchone()[0]
#         if playerid!=pid:
#             return HttpResponse("not allowed")
        
        cursor.execute("select * from player where playerid = %s"%(pid))
        profileinfo=cursor.fetchone()
        c["profileinfo"]=profileinfo
        cursor.execute("select * from comments where commenterid = %s order by comment_time desc"%(pid))
        c["comments"]=cursor.fetchall()
        cursor.execute("select * from reviews where playerid     = %s order by review_time desc"%(pid))
        c["reviews"]=cursor.fetchall()
        cursor.execute("select o.*, title from ordergame o,game where o.playerid=%s and o.gameid=game.gameid"%(pid))
        c["orders"]=cursor.fetchall()
    return render_to_response("playerhistory.html",c)

# Searching game
def searchGame(request):
    c={}
    conn=mdb.connect(host='localhost',user='htoowaiyan', passwd='Admin@12345',db='game_community')
    if 'title' in request.GET:
        title=request.GET['title']
        genre=request.GET['genre']
        sort=request.GET['sort']
        if title=="":
            c["notitle"]=True
            return render_to_response('searchgame.html',c)
        
        else:
            with conn:
                cursor=conn.cursor()
                query="select * from game where title like '%%%s%%'"%(title)
                if genre!="":
                    query=query+" and genre= '%s'"%(genre)
                query=query+" order by '%s'"%(sort)
                
                 
                 
                cursor.execute(query)
                if cursor.rowcount==0:
                    raise Http404("Game not found")
                else:
                    gamelist = cursor.fetchall()
                    c["gamelist"]=gamelist
                    render_to_response('searchgame.html',c)
    return render_to_response('searchgame.html',c)

# User feedback review the game
def gamePage(request,gid):  
    c = {}   
    c["gid"]=gid
    conn=mdb.connect(host='localhost',user='htoowaiyan', passwd='Admin@12345',db='game_community')
    with conn:
        cursor=conn.cursor()
        cursor.execute("select * from game where gameid= %s"%(gid))
        if cursor.rowcount==0:
            Http404("game not found")
        cursor.execute("select playerid from player where loginname= '%s'"%(request.user.username))
        playerid=cursor.fetchone()[0]
        cursor.execute("Select * from reviews where playerid=%s and gameid=%s"%(playerid,gid))
        if cursor.rowcount==1:
            c["reviewed"]=True
        else:
            c["reviewed"]=False
        cursor.execute("Select * from rate_game where playerid=%s and gameid=%s"%(playerid,gid))
        if cursor.rowcount==1:
            c["rated"]=True
        else:
            c["rated"]=False
    if request.user.is_authenticated():
        c["auth"]=True
    
    c.update(csrf(request))
    if 'review' in request.POST:
        review=request.POST["review"]
        
        if review=="":
            c["noreview"]=True
            return render(request,"gamepage.html",c)
        else:
            with conn:
                cursor=conn.cursor()
                try:
                    
                    cursor.execute("insert into reviews(playerid,gameid,review,review_time) values(%s,%s,'%s','%s')"%(playerid,gid,review,datetime.datetime.now()))
                except MySQLdb.IntegrityError as e:
                    cursor.execute("Select * from reviews;")
                    row=cursor.rowcount
                    c["reviewed"]=True
                    cursor.execute("ALTER TABLE reviews AUTO_INCREMENT=%s"%(str(row)))
                    return render(request,"gamepage.html",c)
                c["reviewed"]=True
                return render(request,"gamepage.html",c)
    if 'rating' in request.POST:
        rating=request.POST["rating"]
        
        if rating=="":
            c["noreview"]=True
            return render(request,"gamepage.html",c)
        else:
            with conn:
                cursor=conn.cursor()
                try:
                    cursor.execute("insert into rate_game(playerid,gameid,gamescore) values(%s,%s,%s)"%(playerid,gid,rating))
                    cursor.execute("update game set score=(select AVg(gamescore) from rate_game where gameid=%s) where gameid=%s"%(gid,gid))
                except MySQLdb.IntegrityError as e:
                    return render(request,"gamepage.html",c)
                c["rated"]=True
                return render(request,"gamepage.html",c)
    return render(request,"gamepage.html",c)

# reveiw page
def review(request,gid):
    c={}
    c["gid"]=gid
    conn=mdb.connect(host='localhost',user='htoowaiyan', passwd='Admin@12345',db='game_community')
    with conn:
        cursor=conn.cursor()
        cursor.execute("select * from game where gameid= %s"%(gid))
        game=cursor.fetchone()
        cursor.execute("select loginname, review from reviews,player where reviews.gameid=%s and reviews.playerid=player.playerid"%(gid))
        reviewlist=cursor.fetchall()
    c["title"]=game[1]
    c["score"]=game[5]
    c["reviewlist"]=reviewlist
    if "generate" in request.GET:
        c["generate"]= request.GET["generate"]
    return render_to_response("review_game.html",c)
      
# player page
def player(request,pid):
    c={}
    c.update(csrf(request))
    c["pid"]=pid
    conn=mdb.connect(host='localhost',user='htoowaiyan', passwd='Admin@12345',db='game_community')
    if "comment" in request.POST:
        with conn:
            cursor=conn.cursor()
            cursor.execute("select * from player where loginname='%s'"%(request.user.username))
            commenterid=cursor.fetchone()[0]
            comment=request.POST["comment"]
            cursor.execute("insert into comments(commenterid,receiverid,comment_content,comment_time) values(%s,%s,'%s','%s')"%(commenterid,pid,comment,datetime.datetime.now()))
            
    with conn:
        cursor=conn.cursor()
        cursor.execute("select * from player where playerid= %s"%(pid))
        player=cursor.fetchone()
        cursor.execute("select * from game")
        games=cursor.fetchall()
        cursor.execute("select loginname, receiverid, comment_content,commenterid from comments, player where player.playerid=comments.commenterid and receiverid=%s"%(pid))
        comments=cursor.fetchall()
        
    c["name"]=player[1]
    c["score"]=player[4]
    c["gamelist"]=games
    c["comments"]=comments
    if "challenge" in request.GET:
        challengegame=request.GET["challengegame"]
        with conn:
            cursor=conn.cursor()
            cursor.execute("select playerid from player where loginname= '%s'"%(request.user.username))
            challengerid=cursor.fetchone()[0]
            cursor.execute("select gameid from game where title= '%s'"%(challengegame))
            gameid=cursor.fetchone()[0]
            cursor.execute("insert into challenges(accepterid,gameid,challengerid,cha_time,outcome) values(%s,%s,%s,'%s','pending')"%(pid,gameid,challengerid,datetime.datetime.now()))
        return redirect("/game/%s/challenge"%(gameid))
        
        
        
    return render_to_response("playerpage.html",c)

# issue challenge
@login_required(login_url='/login/')
def challenge(request,gid):
    c={}
    c.update(csrf(request))
    conn=mdb.connect(host='localhost',user='htoowaiyan', passwd='Admin@12345',db='game_community')
    with conn:
        cursor=conn.cursor()
        cursor.execute("select playerid from player where loginname= '%s'"%(request.user.username))
        playerid=cursor.fetchone()[0]
        cursor.execute("select c.* ,loginname from challenges c, player where challengerid=%s and outcome='pending' and c.accepterid=player.playerid"%(playerid))
        c["pending"]=cursor.fetchall()
        cursor.execute("select c.* ,loginname from challenges c, player where accepterid=%s and outcome='pending' and c.challengerid=player.playerid"%(playerid))
        c["waiting"]=cursor.fetchall()
    if "accept" in request.POST:
        cid=request.POST["accept"]
        with conn:
            cursor=conn.cursor()
            cursor.execute("update challenges set outcome='accepted' where challengeid=%s"%(cid))
    elif "decline" in request.POST:
        cid=request.POST["decline"]
        with conn:
            cursor=conn.cursor()
            cursor.execute("update challenges set outcome='declined' where challengeid=%s"%(cid))
    elif "cancel" in request.POST:
        cid=request.POST["cancel"]
        with conn:
            cursor=conn.cursor()
            cursor.execute("update challenges set outcome='canceled' where challengeid=%s"%(cid))
    return render(request,"challenge.html",c)

# 
