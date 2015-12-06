from django.shortcuts import render,render_to_response,redirect
from django.http import HttpResponse,Http404,HttpRequest
from django.template.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext
import MySQLdb as mdb
import datetime
import MySQLdb
from django.contrib.redirects.models import Redirect

# Create your views here.

# Registration
def register(request):
    
    if "loginname" in request.GET:
        conn=mdb.connect(host='localhost',user='htoowaiyan', passwd='Admin@12345',db='game_community')
        with conn:
            cursor=conn.cursor()
            
            try:
                cursor.execute("insert into player(loginname) values('adad')")
            except MySQLdb.IntegrityError as e:
                cursor.execute("Select * from player;")
                row=cursor.rowcount
                cursor.execute("ALTER TABLE player AUTO_INCREMENT=%s"%(str(row)))
                return HttpResponse("duplicate name")
    
        return HttpResponse("Register player")
    else:
        return render(request,'register.html')

# Login
def login(request):
    if "loginname" in request.GET:
        username="Admin"
        password="Admin@12345"
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            return HttpResponse("login complete")
    
        return HttpResponse("Register player")
    else:
        return render(request,'register.html')
        
# Ordering new game
@login_required(login_url='/login/')
def orderGame(request):
    conn=mdb.connect(host='localhost',user='htoowaiyan', passwd='Admin@12345',db='game_community')
    c={}
    c.update(csrf(request))
    if 'gameid' in request.POST:
        gameid=request.POST['gameid']
        if gameid=="":
            
            norequest=True
            c["norequest"]=norequest
            return render_to_response('ordernewgame.html',c)
        else:
            with conn:
                cursor=conn.cursor()
                cursor.execute("select playerid from player where loginname= '%s'"%(request.user.username))
                pid=cursor.fetchone()[0]
                cursor.execute("insert into ordergame(playerid,gameid,numoforder) values(%s,%s,1)"%(pid,gameid))
                if cursor.rowcount==0:
                    raise Http404("Player not found")
                else:
                    row = cursor.fetchone()
                return render_to_response('added.html',c)
    
    else:
        return render_to_response('ordernewgame.html',c)
    
    return render_to_response('addnewgame.html')

# Add new game
@login_required(login_url='/login/')
def addNewGame(request):
    username=request.user.username
    if username != "Admin":
        return HttpResponse("only admin is allowed to add")
    c = {}
    c.update(csrf(request))
    
    if 'gameid' in request.POST:
        gameid=request.POST['gameid']
    
        if gameid=="":
            
            norequest=True
            c["norequest"]=norequest
            return render_to_response('addnewgame.html',c)
        else:
             
            return HttpResponse("haha")
    
    else:
        return render_to_response('addnewgame.html',c)


def index(request):
    return render_to_response("index.html",context_instance=RequestContext(request))

# Search player 
def searchPlayer(request,pid):
    conn=mdb.connect(host='localhost',user='htoowaiyan', passwd='Admin@12345',db='game_community')
    with conn:
        cursor=conn.cursor()
        cursor.execute("select * from player where playerid = %s"%(pid))
        if cursor.rowcount==0:
            raise Http404("Player not found")
        else:
            row = cursor.fetchone()
            context={'pid':row[0]}
    if "submit" in request.GET:
        if request.GET["submit"]=="get":
            return redirect('/player/%s'%(row[0]))      
    return render(request,'searchplayer.html',context)



# User Record
def getUserRecord(request, pid):
    conn=mdb.connect(host='localhost',user='htoowaiyan', passwd='Admin@12345',db='game_community')
    with conn:
        cursor=conn.cursor()
        cursor.execute("select * from player where playerid = %s"%(pid))
        if cursor.rowcount==0:
            raise Http404("Player not found")
        else:
            row = cursor.fetchone()
    return HttpResponse("Playerid: %s \nPlayerPasword: %s"%(row[0],row[1]))

# Searching game
def searchGame(request):
    conn=mdb.connect(host='localhost',user='htoowaiyan', passwd='Admin@12345',db='game_community')
#     if len(request.GET)==1:
    if 'title' in request.GET:
        gameid=request.GET['gameid']
        title=request.GET['title']
        developer=request.GET['developer']
        sort=request.GET['sort']
        order=request.GET['order']
        if title=="":
            
            norequest=True
            return render_to_response('searchgame.html',{"norequest":norequest})
        else:
            with conn:
                cursor=conn.cursor()
                query="select * from game where title = '%s'"%(title)
                if developer!="":
                    
                    query=query+" and developer= %s"%(developer)
                query=query+" order by %s"%(sort)
                if order!="asce":
                    query=query+" %s"%(order)
                
                
                cursor.execute(query)
                if cursor.rowcount==0:
                    raise Http404("Game not found")
                else:
                    rows = cursor.fetchall()
                    result=""
                    for i in range(len(rows)):
                        result=result+str(rows[i])+"\n"
                    return HttpResponse("got it %s"%(result))
    return render_to_response('searchgame.html')

# User feedback review the game
def gamePage(request,gid):  
    c = {}   
    conn=mdb.connect(host='localhost',user='htoowaiyan', passwd='Admin@12345',db='game_community')
    with conn:
        cursor=conn.cursor()
        cursor.execute("select * from game where gameid= %s"%(gid))
        if cursor.rowcount==0:
            Http404("game not found")
    if request.user.is_authenticated():
        c["auth"]=True
    
    c.update(csrf(request))
    if 'comment' in request.POST:
        comment=request.POST["comment"]
        rating=request.POST["rating"]
        if comment=="":
            c["jaja"]=True
            return render(request,"gamepage.html",c)
        else:
            with conn:
                cursor=conn.cursor()
                try:
                    cursor.execute("insert into reviews(playerid,gameid,review,review_time,rating) values(1,%s,'%s','%s',%s)"%(gid,comment,datetime.datetime.now(),rating))
                except MySQLdb.IntegrityError as e:
                    cursor.execute("Select * from reviews;")
                    row=cursor.rowcount
                    c["reviewed"]=True
                    cursor.execute("ALTER TABLE reviews AUTO_INCREMENT=%s"%(str(row)))
                    return render(request,"gamepage.html",c)
                c["reviewed"]=True
                return render(request,"gamepage.html",c)
    # need to check the userid from request.user before httpresponse
    c["shishi"]=True
    with conn:
        cursor=conn.cursor()
        cursor.execute("select review from reviews order by rating desc;")
        
    
    return render(request,"gamepage.html",c)
   
# player page
def player(request,pid):
    return HttpResponse("player page")

# issue challenge
def challenge(request):
    if "submit" in request.GET:
        return redirect("/challenge")
    
    return render(request,"challenge.html")

# 
