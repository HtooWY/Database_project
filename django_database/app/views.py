from django.shortcuts import render,render_to_response
from django.http import HttpResponse,Http404,HttpRequest
import MySQLdb as mdb
import datetime

# Create your views here.

def hello(request):
    return HttpResponse("Hello, this is django")

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

# Registration
def Register(request, pid, password):
    conn=mdb.connect(host='localhost',user='htoowaiyan', passwd='Admin@12345',db='game_community')
    with conn:
        cursor=conn.cursor()
        cursor.execute("Insert into player values(%s, %s, %s, 0)"%(pid,password,datetime.datetime.now()))
    
    return HttpRequest("Register player")

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

# Add new game
def AddNewGame(request):
    norequest=False
    if 'gameid' in request.POST:
        gameid=request.POST['gameid']
    if 'gameid' not in request.POST:
        norequest=True
    else:
        return render_to_response('Added.html')
    return render_to_response('addnewgame.html',{'norequest':norequest})
     
            