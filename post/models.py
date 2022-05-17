from django.db import models

# Create your models here.
class Post(models.Model):

    title = models.CharField(max_length=200)
    content = models.TextField()

class Audio(models.Model):
    
    audio = models.FileField(upload_to='audio/')