from django.conf.urls import url,re_path
from django.urls import path
from . import consumer

websocket_urlpatterns = [
 path('ws/chat/<str:id1>/', consumer.ChatConsumer),
]