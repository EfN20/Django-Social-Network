import os

from django.db import models
from users.models import User

from datetime import datetime


class Media(models.Model):
    file = models.FileField(upload_to="stories/")
    text = models.TextField(max_length=64, blank=True)
    posted_date = models.DateTimeField(default=datetime.now())
    user = models.ForeignKey(User, related_name="story_user", on_delete=models.CASCADE)

    def extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension
