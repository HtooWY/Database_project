'''
Created on Nov 27, 2015

@author: Wai Yan
'''
from django.conf.urls import url
from . import views

urlpatterns =[
    url(r'^$',views.index,name='index'),
    url(r'^register/$',views.Register,name="register"),
    url(r'^login/$',views.Login,name="login"),
    url(r'^addnewgame/$',views.AddNewGame,name="addnewgame"),
    url(r'^searchplayer/(.{0,9})/$',views.searchplayer,name="searchplayer"),
    
    
    url(r'^order/$',views.OrderGame,name="ordergame"),
    url(r'^searchgame/$',views.SearchGame,name="searchgame"),
#     url(r'order/$',views.OrderGame,name="ordergame")
]
