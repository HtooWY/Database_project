'''
Created on Nov 27, 2015

@author: Wai Yan
'''
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns =[
    url(r'^$',views.index,name='index'),
    url(r'^register/$',views.register,name="register"),
    url(r'^login/$',views.login,name="login"),
    url(r'^addnewgame/$',views.addNewGame,name="addnewgame"),
    url(r'^game/(.{0,9})/reviews/$',views.review,name="review"),
    url(r'^game/(.{0,9})/order/$',views.orderGame,name="ordergame"),
    url(r'^game/(.{0,9})/challenge/$',views.challenge,name="challenge"),
    url(r'^logout/$',views.logout,name='logout'),
    url(r'^game/(.{0,9})/$',views.gamePage,name="game"),
    url(r'^player/(.{0,9})/record/$',views.getUserRecord,name="profile"),
    url(r'^player/(.{0,9})/$',views.player,name="player"),
#     url(r'^game/(.{0,9})/',include([url(r'^$',views.gamePage,name="game"),url(r'^reviews/$',views.review,name="review")])),
    url(r'^searchplayer/$',views.searchPlayer,name="searchplayer"),
#     url(r'^order/$',views.orderGame,name="ordergame"),
    url(r'^searchgame/$',views.searchGame,name="searchgame"),
    
#     url(r'order/$',views.OrderGame,name="ordergame")
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
