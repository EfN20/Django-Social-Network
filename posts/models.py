from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.conf import settings


class Post(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(default='')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post_date = models.DateTimeField(default=datetime.now())
    img = models.ImageField(upload_to='posts/', blank=True)
    medias = models.ManyToManyField('medias.Media')
