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
            
            return redirect("/order")
        c["notfound"]=True
        return render(request,'login.html',c)
    else:
        return render(request,'login.html',c)
        
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
        cursor.execute("select playerid from player where loginname= '%s'"%(request.user.username))
        playerid=cursor.fetchone()[0]
        cursor.execute("Select * from reviews where playerid=%s and gameid=%s"%(playerid,gid))
        if cursor.rowcount==1:
            c["reviewed"]=True
        else:
            c["reviewed"]=False
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
    #
        
    
    return render(request,"gamepage.html",c)
   
# player page
def player(request,pid):
    return HttpResponse("player page")

# issue challenge
@login_required(login_url='/login/')
def challenge(request):
    if "submit" in request.GET:
        return redirect("/challenge")
    
    return render(request,"challenge.html")

# 
