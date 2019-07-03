from django.conf.urls import url,include
from django.contrib import admin
from chat import views
from django.urls import include, path
urlpatterns = [
    path('', views.index, name='chat'),
    path('<str:id1>/',views.room,name="room"),
    path('profile/<str:id1>/',views.profileView.as_view(),name="profile")
]