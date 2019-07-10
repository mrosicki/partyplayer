from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('playerpage', views.playerpage, name='playerpage'),
    path('login', views.loginpage, name='playerpage'),
    path('add_song', views.add_song, name='add_song'),

]