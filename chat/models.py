from django.db import models
from users.models import User
from datetime import datetime


class Room(models.Model):
    name = models.CharField(max_length=64)
    type = models.BooleanField(default=False)
    members = models.ManyToManyField(User, symmetrical=False)


class Message(models.Model):
    user = models.ForeignKey(User, related_name='user_id', on_delete=models.CASCADE)
    room = models.ForeignKey(Room, related_name='room_id', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='chat/', blank=True)
    text = models.CharField(max_length=128, blank=True)
    date = models.DateTimeField(default=datetime.now())
