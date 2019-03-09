from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class Topic(models.Model):
    title = models.CharField(max_length=1000)
    url = models.CharField(max_length=500)
    byline = models.CharField(max_length=200)
    published_date = models.DateField()
    abstract = models.CharField(max_length=2500)

    def __str__(self):
        return self.title
    
    def get_top_level_posts(self):
        return self.posts.filter(parent__isnull=True)

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    date = models.DateField(auto_now_add=True)
    text = models.TextField(max_length=10000)
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT, related_name='posts')
    parent = models.ForeignKey('self', null=True, blank=True, default=None, on_delete=models.PROTECT, related_name='children')

    def __str__(self):
        return self.text



