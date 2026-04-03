import json
from django.shortcuts import render
from django.db import connection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_articles(request):
    current_user_id = request.user.id
    with connection.cursor() as cursor:
        cursor.execute("""SELECT DISTINCT Article.* FROM Article
        JOIN Article_Tags 
        ON Article.id = Article_Tags.article_id
        JOIN TAG 
        ON Article_Tags.tag_id = Tag.id
        JOIN User_Tag
        WHERE Tag.id = User_Tag.tag_id
        AND User_Tag.user_id = %s""", [current_user_id])
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

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def bookmark_article(request):
    current_user_id = request.user.id
    payload = json.loads(request.body)
    
    with connection.cursor() as cursor:
        cursor.execute("""INSERT INTO BOOKMARK (user_id, article_id) VALUES ()""")
                       
    return JsonResponse("success")