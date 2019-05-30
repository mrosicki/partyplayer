from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('playerpage', views.playerpage, name='playerpage'),
    path('login', views.login, name='playerpage'),

]