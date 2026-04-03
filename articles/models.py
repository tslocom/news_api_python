from django.db import models
from django.contrib.auth.models import User

class Publication(models.Model):
    class Meta:
        db_table = 'Publication'
    name = models.CharField(max_length=256)
    publication_link = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    
class Tag(models.Model):
    class Meta:
        db_table = 'Tag'
    name = models.CharField(max_length=64, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
class UserTag(models.Model):
    class Meta:
        db_table = 'User_Tag'
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    is_ignored = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Article(models.Model):
    class Meta:
        db_table = 'Article'
    title = models.CharField(max_length=256 , db_index=True)
    summary = models.TextField()
    article_link = models.URLField()
    published_at = models.DateTimeField()
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    author = models.CharField(max_length=256, null=True, blank=True)
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)
    
class Bookmark(models.Model):
    class Meta:
        db_table = 'Bookmark'
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

