from django.db import models
from users.models import User


class Media(models.Model):
    name = models.CharField(max_length=255)
    url = models.TextField()
    file = models.FileField(upload_to='media/')
