from django.shortcuts import render
from django.db import connection
from django.http import JsonResponse

# Create your views here.
def get_articles(request):
    with connection.cursor() as cursor:
        cursor.execute("""SELECT DISTINCT * FROM ARTICLES_ARTICLE
        JOIN ARTICLES_ARTICLE_TAGS 
        ON ARTICLES_ARTICLE.id = ARTICLES_ARTICLE_TAGS.article_id
        JOIN ARTICLES_ALL_TAG 
        ON ARTICLES_ARTICLE_TAGS.all_tag_id = ARTICLES_ALL_TAG.id
        WHERE ARTICLES_ALL_TAG.name IN (
            SELECT name FROM ARTICLES_USER_TAG
            )""")
        raw_article_data = cursor.fetchall()
        formatted_article_data = []
        for row in raw_article_data:
            article_dict = {
                "id": row[0],
                "title": row[1],
                "summary": row[2],
                "link": row[3],
                "date": row[4],
                "publisher": row[5],
                "author": row[6],
                "tags": row[7],
            }
            
            formatted_article_data.append(article_dict)
        
    return JsonResponse({"articles": formatted_article_data})