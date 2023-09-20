from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class BlogPost(models.Model):
    image= models.ImageField(upload_to='gallery/')
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    

class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    
