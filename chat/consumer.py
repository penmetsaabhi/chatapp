# chat/consumers.py
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import  Message,USERIMAGE
from django.contrib.auth.models import User
import json

class ChatConsumer(WebsocketConsumer):
    def fetch_messages(self,context):
        message=Message.last_10_messages()
        context={
            'command' : 'messages',
            'messages' : self.make_messages_to_json(message),
        }
        self.send_message(context)
    def new_message(self,context):
        author=context['from']
        user=User.objects.get(username=author)
        try:
            userimg = USERIMAGE.objects.all().filter(user=user).order_by('-id')[0]
        except IndexError:
            userimg = None
        print(userimg)
        if(context['message']!=""):
            message=Message.objects.create(
            author=user,
            context=context['message']
        )
            content={
            'command':'new_message',
            'message':self.make_message_to_json(message),
            'img':str(userimg.usr_Img.url),

        }
            return self.send_chat_message(content)
    commands={
        'fetch_messages':fetch_messages,
        'new_message':new_message

    }
    def make_messages_to_json(self,messages):
        result=[]
        for message in messages:
            result.append(self.make_message_to_json(message))
        return  result
    def make_message_to_json(self,message):
        return {
            'author': message.author.username,
            'context': message.context,
            'timestamp': str(message.timestamp)
        }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['id1']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self,data)
    def send_chat_message(self,message):
        # Send message to room group

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
            }
        )
    def send_message(self,message):
        self.send(text_data=json.dumps(message))
    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))