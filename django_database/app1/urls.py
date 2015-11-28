'''
Created on Nov 27, 2015

@author: Wai Yan
'''

from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$',views.hello,name='hello'),
#     url(r'^$', views.hello, name='hello'),
#     url(r'^searchfaculty/(.{3,9})/$',views.searchfaculty,name='searchfaculty'),  
#     url(r'^searchcourse/(.{3,9})/$',views.searchcourse,name='searchcourse'), 
#     url(r'^searchteach/$',views.searchteach,name='searchteach'),   
]
