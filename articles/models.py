from django.db import models
from django.contrib.auth.models import User

class Publication(models.Model):
    class Meta:
        db_table = 'publication'
    name = models.CharField(max_length=256, unique=True)
    publication_link = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    
class UserPublication(models.Model):
    class Meta:
        db_table = 'user_publication'
        constraints = [models.UniqueConstraint(fields=['user', 'publication'], name='unique_user_publications')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
class Tag(models.Model):
    class Meta:
        db_table = 'tag'
    name = models.CharField(max_length=128, db_index=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
class UserTag(models.Model):
    class Meta:
        db_table = 'user_tag'
        constraints = [models.UniqueConstraint(fields=['user', 'tag'], name='unique_user_tags')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    is_ignored = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Article(models.Model):
    class Meta:
        db_table = 'article'
    title = models.CharField(max_length=256 , db_index=True)
    summary = models.TextField()
    link = models.URLField(unique=True)
    published_at = models.DateTimeField()
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    author = models.CharField(max_length=256, null=True, blank=True)
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)
    
class Bookmark(models.Model):
    class Meta:
        db_table = 'bookmark'
        constraints = [models.UniqueConstraint(fields=['user', 'article'], name='unique_user_bookmarks')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

