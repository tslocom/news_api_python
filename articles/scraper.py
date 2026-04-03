import sys
import os
import django
import feedparser

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_api_python.settings')

django.setup()

from articles.models import Publication, UserTag, Article
from django.db import connection

with connection.cursor() as cursor: #uncomment this to run below queries on first test
    #cursor.execute("INSERT INTO PUBLICATION (name, publication_link, created_at) VALUES ('TechCrunch', 'www.techcrunch.com', CURRENT_TIMESTAMP)") #uncomment this if you are running this locally for the first time, this adds TechCrunch to the database as it is the single source for right now
    #cursor.execute("INSERT INTO USER_TAG (tag_id, user_id, is_ignored, created_at) VALUES (65, 2, 0, CURRENT_TIMESTAMP)") #uncomment these to populate your preferred tags table for testing, '65' which correlates to apple can be changed to any id in the tag table
    cursor.execute("INSERT INTO USER_TAG (tag_id, user_id, is_ignored, created_at) VALUES ('3', 1, False, CURRENT_TIMESTAMP)") #uncomment these to populate your preferred tags table for testing, '3' which correlates to ai can be changed to any id in the tag table
    #cursor.execute("INSERT INTO USER_TAG (name, is_ignored, created_at) VALUES ('tech', False, CURRENT_TIMESTAMP)") #uncomment these to populate your preferred tags table for testing, 'tech' can be changed to any tech related keyword
    
techcrunch_feed = feedparser.parse("https://techcrunch.com/feed/")

for entry in techcrunch_feed.entries:
    if not entry.get("tags", []):
        continue
    with connection.cursor() as cursor:
        sql_string = "INSERT INTO ARTICLE (title, summary, article_link, published_at, publication_id, author, created_at) VALUES (%s, %s, %s, %s, 1, %s, CURRENT_TIMESTAMP)"
        
        data_values = [entry.get("title", ""), entry.get("summary", ""), entry.get("link", ""), entry.get("published", ""), entry.get("author", ""),]
        cursor.execute(sql_string, data_values)
        article_tags = entry.get("tags", [])
        new_article_id = cursor.lastrowid
        for tag in article_tags:
            sql_string = "INSERT INTO TAG (name, created_at) VALUES (%s, CURRENT_TIMESTAMP)"
            
            data_values = [tag.get("term", "").lower(),]
            cursor.execute(sql_string, data_values)
            
            new_tag_id = cursor.lastrowid
            junction_string = "INSERT INTO ARTICLE_TAGS (tag_id, article_id) VALUES (%s, %s)"
            junction_values = [new_tag_id, new_article_id]
            cursor.execute(junction_string, junction_values)
            