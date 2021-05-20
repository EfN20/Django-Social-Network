from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.conf import settings


class Post(models.Model):
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(default='', blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post_date = models.DateTimeField(default=datetime.now().strftime("%d-%m-%Y %H:%M"))
    img = models.ImageField(upload_to='posts/', blank=True)
    medias = models.ManyToManyField('medias.Media')

    def delete(self, using=None, keep_parents=False):
        self.img.delete()
        super().delete()
