from distutils.command import upload
from django.db import models
import urllib
import os
from django.core.files import File

# Create your models here.
class Post(models.Model):

    title = models.CharField(max_length=200)
    content = models.TextField()

class Sound(models.Model):
    
    audio_file = models.FileField(upload_to='sounds/')
    audio_url = models.URLField()
    
    def get_remote_file(self):
        
        if self.audio_url and not self.audio_file:
            result = urllib.request.urlretrieve(self.audio_url)
            self.audio_file.save(
                os.path.basename(self.audio_url),
                File(open(result[0]))
            )
            self.save()