'''
Created on Nov 27, 2015

@author: Wai Yan
'''
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns =[
    url(r'^$',views.index,name='index'),
    url(r'^register/$',views.register,name="register"),
    url(r'^login/$',views.login,name="login"),
    url(r'^addnewgame/$',views.addNewGame,name="addnewgame"),
    url(r'^game/(.{0,9})/$',views.gamePage,name="game"),
    url(r'^searchplayer/(.{0,9})/$',views.searchPlayer,name="searchplayer"),
    url(r'^player/(.{0,9})/$',views.player,name="player"),
    url(r'^order/$',views.orderGame,name="ordergame"),
    url(r'^searchgame/$',views.searchGame,name="searchgame"),
    url(r'^challenge/$',views.challenge,name="challenge"),
#     url(r'order/$',views.OrderGame,name="ordergame")
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
