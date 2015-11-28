'''
Created on Nov 27, 2015

@author: Wai Yan
'''
from django.conf.urls import url

from . import views
urlpatterns =[
    url(r'^$', views.hello, name="hello"),
    url(r'^searchplayer/(.{0,9})/$',views.searchplayer,name="searchplayer"),
    url(r'addnewgame/$',views.AddNewGame,name="addnewgame"),
]
