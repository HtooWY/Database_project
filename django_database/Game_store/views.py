from django.shortcuts import render,render_to_response
from django.http import HttpResponse,Http404,HttpRequest
from django.template.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
import MySQLdb as mdb
import datetime
import MySQLdb

# Create your views here.

# Registration
def Register(request):
    
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
def Login(request):
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
def OrderGame(request):
    conn=mdb.connect(host='localhost',user='htoowaiyan', passwd='Admin@12345',db='game_community')
    if 'gameid' in request.POST:
        gameid=request.GET['gameid']
        if gameid=="":
            
            norequest=True
            return render_to_response('searchgame.html',{"norequest":norequest})
        else:
            with conn:
                cursor=conn.cursor()
                cursor.execute("select * from order where orderid = %s"%(gameid))
                if cursor.rowcount==0:
                    raise Http404("Player not found")
                else:
                    row = cursor.fetchone()
    
    else:
        return render_to_response('Added.html')
    
    return render_to_response('addnewgame.html')

# Add new game
@login_required(login_url='/login/')
def AddNewGame(request):
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
    return HttpResponse("Hello, this is django database sdfsdf")

def searchplayer(request,pid):

    conn=mdb.connect(host='localhost',user='htoowaiyan', passwd='Admin@12345',db='game_community')
    with conn:
        cursor=conn.cursor()
        cursor.execute("select * from player where playerid = %s"%(pid))
        if cursor.rowcount==0:
            raise Http404("Player not found")
        else:
            row = cursor.fetchone()
            context={'pid':row[0]}   
            
    return render(request,'searchplayer.html',context)



# User Record
def GetUserRecord(request, pid):
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
def SearchGame(request):
    conn=mdb.connect(host='localhost',user='htoowaiyan', passwd='Admin@12345',db='game_community')
    if 'gameid' in request.GET:
        gameid=request.GET['gameid']
        if gameid=="":
            
            norequest=True
            return render_to_response('searchgame.html',{"norequest":norequest})
        else:
            with conn:
                cursor=conn.cursor()
                cursor.execute("select * from game where gameid = %s"%(gameid))
                if cursor.rowcount==0:
                    raise Http404("Game not found")
                else:
                    row = cursor.fetchone()
                    return HttpResponse("got it %s"%(row[1]))
    
    
    return render_to_response('searchgame.html')

# 
    
