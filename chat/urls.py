from django.conf.urls import url,include
from django.contrib import admin
from chat import views
from django.urls import include, path
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:id1>/',views.room,name="room")
]