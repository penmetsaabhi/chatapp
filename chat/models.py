from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

user=get_user_model()

class Message(models.Model):
    author=models.ForeignKey(user,related_name="author_message",on_delete=models.CASCADE)
    context=models.TextField(max_length=1000)
    timestamp=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.author.username

    def last_10_messages():
        return Message.objects.order_by('-timestamp')[:10]