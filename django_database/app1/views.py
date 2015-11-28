from django.shortcuts import render, render_to_response

# Create your views here.
from django.http import HttpResponse, Http404
import MySQLdb as mdb
from django.db.models import F
from models import teach

def hello(request):
    return HttpResponse("Hello, world. This is tutorial 3!!!")

def searchfaculty(request, fid):
    conn = mdb.connect (host = "localhost",user = "htoowaiyan",passwd = "Admin@12345",db = "tutorial")
    with conn:
        cursor = conn.cursor ()
        cursor.execute ("select fname from app1_faculty where fid = '%s'"%(fid))
        if cursor.rowcount==0:
            raise Http404("Facuty does not exist")
        else:
            row=cursor.fetchone()
            html="You're searching Prof. '%s' with id '%s'." % (row[0],fid)
    return HttpResponse(html)

def searchcourse(request, cid):
    conn = mdb.connect (host = "localhost",user = "htoowaiyan",passwd = "Admin@12345",db = "tutorial")
    with conn:
        cursor = conn.cursor ()
        cursor.execute ("select cname,credits from app1_course where cid = '%s'"%(cid))
        if cursor.rowcount==0:
            raise Http404("Course does not exist")
        else:
            row=cursor.fetchone()
            context={'cid':cid,'cname':row[0],'credits':row[1]}     
    return render(request,'cname.html',context)

def searchteach(request):
    error = False
    cid=None
    if 'cnum' in request.GET:
        cid = request.GET['cnum']
    if not cid:
        error = True
    else:
        sections = teach.objects.filter(cid__exact=cid).filter(enrollment__lt=F('capacity'))
        return render_to_response('search_result.html',{'sections': sections, 'query': cid})
    return render_to_response('search_form.html', {'error': error})