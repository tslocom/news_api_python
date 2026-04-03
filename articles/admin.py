from django.contrib import admin

from .models import Article, Bookmark, Publication, Tag, UserTag

admin.site.register([Article, Bookmark, Publication, Tag, UserTag])
