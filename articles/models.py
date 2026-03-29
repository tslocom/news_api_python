from django.db import models

class Publication(models.Model):
    name = models.CharField(max_length=256)
    publication_link = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    
class All_Tag(models.Model):
    name = models.CharField(max_length=64, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
class User_Tag(models.Model):
    name = models.CharField(max_length=64, db_index=True)
    is_ignored = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Article(models.Model):
    title = models.CharField(max_length=256, db_index=True)
    summary = models.TextField()
    article_link = models.URLField()
    published_at = models.DateTimeField()
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    author = models.CharField(max_length=256, null=True, blank=True)
    tags = models.ManyToManyField(All_Tag)
    created_at = models.DateTimeField(auto_now_add=True)
    
class Bookmark(models.Model):
    title = models.CharField(max_length=256, db_index=True)
    summary = models.TextField()
    article_link = models.URLField()
    published_at = models.DateTimeField()
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    author = models.CharField(max_length=256, null=True, blank=True)
    tags = models.ManyToManyField(All_Tag)
    created_at = models.DateTimeField(auto_now_add=True)

