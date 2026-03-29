from django.contrib import admin

from .models import Article, Bookmark, Publication, All_Tag, User_Tag

admin.site.register([Article, Bookmark, Publication, All_Tag, User_Tag])
