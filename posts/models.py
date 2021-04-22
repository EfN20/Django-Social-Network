from _datetime import *

from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.TextField(default='')
    text = models.TextField(default='')
    date = models.DateTimeField(default=datetime.now())
    img = models.ImageField(upload_to='', blank=True)