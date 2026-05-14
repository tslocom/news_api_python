import json
from django.shortcuts import render
from django.db import connection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_articles(request):
    current_user_id = request.user.id
    with connection.cursor() as cursor:
        cursor.execute("""SELECT article.id, article.title, article.summary, article.link, article.published_at, article.author, GROUP_CONCAT(publication.name) as matched_pubs,
                            GROUP_CONCAT(tag.name) as matched_tags FROM article
                            JOIN publication 
                            ON article.publication_id = publication.id
                            JOIN user_publication
                            ON publication.id = user_publication.publication_id
                            JOIN article_tags 
                            ON article.id = article_tags.article_id
                            JOIN tag 
                            ON article_tags.tag_id = tag.id
                            JOIN user_tag
                            ON tag.id = user_tag.tag_id
                            WHERE user_publication.user_id = %s
                            AND user_tag.is_ignored = False
                            AND user_tag.user_id = %s
                            GROUP BY article.id
                            ORDER BY article.published_at DESC""", [current_user_id, current_user_id])
        raw_article_data = cursor.fetchall()
        formatted_article_data = []
        for row in raw_article_data:
            article_dict = {
                "id": row[0],
                "title": row[1],
                "summary": row[2],
                "link": row[3],
                "date": row[4],
                "author": row[5],
                "publisher": row[6],
                "tags": row[7],
            }
            
            formatted_article_data.append(article_dict)
        
    return JsonResponse({"articles": formatted_article_data})

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def search_articles(request):
    by_tag = request.GET.get('by_tag')
    search_term = request.GET.get('search_term')
    query_term = f"%{search_term}%"
    if by_tag == 'false':
        with connection.cursor() as cursor:
            cursor.execute("""SELECT article.title, article.link, article.published_at, GROUP_CONCAT(DISTINCT tag.name) as matched_tags FROM article
                                JOIN article_tags 
                                ON article.id = article_tags.article_id
                                JOIN tag 
                                ON article_tags.tag_id = tag.id
                                WHERE article.title LIKE %s
                                OR tag.name LIKE %s
                                OR article.summary LIKE %s
                                GROUP BY article.id
                                ORDER BY article.published_at ASC""", [query_term, query_term, query_term])
            raw_article_data = cursor.fetchall()
    else:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT article.title, article.link, article.published_at, GROUP_CONCAT(DISTINCT tag.name) as matched_tags FROM article
                                JOIN article_tags 
                                ON article.id = article_tags.article_id
                                JOIN tag 
                                ON article_tags.tag_id = tag.id
                                WHERE tag.name LIKE %s
                                GROUP BY article.id
                                ORDER BY article.published_at ASC""", [query_term])
            raw_article_data = cursor.fetchall()
    formatted_article_data = []
    for row in raw_article_data:
        article_dict = {
            "title": row[0],
            "link": row[1],
            "date": row[2],
            "tags": row[3],
        }
        formatted_article_data.append(article_dict)
        
        
    return JsonResponse({"articles": formatted_article_data})

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_bookmarks(request):
    current_user_id = request.user.id
    with connection.cursor() as cursor:
        cursor.execute("""SELECT article.id, article.title, article.summary, article.link, article.published_at, article.author, GROUP_CONCAT(tag.name) as matched_tags, GROUP_CONCAT(bookmark.created_at) as bookmark_time FROM article
                            JOIN bookmark 
                            ON article.id = bookmark.article_id
                            JOIN article_tags
                            ON article.id = article_tags.article_id
                            JOIN tag
                            ON article_tags.tag_id = tag.id
                            JOIN user_tag
                            ON tag.id = user_tag.tag_id
                            WHERE user_tag.user_id = %s
                            AND bookmark.user_id = %s
                            GROUP BY article.id
                            ORDER BY bookmark_time """, [current_user_id, current_user_id])
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
def search_bookmarks(request):
    current_user_id = request.user.id
    by_tag = request.GET.get('by_tag')
    search_term = request.GET.get('search_term')
    query_term = f"%{search_term}%"
    if by_tag == 'false':
        with connection.cursor() as cursor:
            cursor.execute("""SELECT article.title, article.link, article.published_at, GROUP_CONCAT(DISTINCT tag.name) as matched_tags, 
                                GROUP_CONCAT(bookmark.created_at) as bookmark_time FROM article
                                JOIN bookmark 
                                ON article.id = bookmark.article_id
                                JOIN article_tags
                                ON article.id = article_tags.article_id
                                JOIN tag
                                ON article_tags.tag_id = tag.id
                                JOIN user_tag
                                ON tag.id = user_tag.tag_id
                                WHERE article.title LIKE %s
                                OR tag.name LIKE %s
                                OR article.summary LIKE %s
                                AND user_tag.user_id = %s
                                AND bookmark.user_id = %s
                                GROUP BY article.id
                                ORDER BY article.published_at ASC""", [query_term, query_term, query_term, current_user_id, current_user_id])
            raw_article_data = cursor.fetchall()
    else:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT article.title, article.link, article.published_at, GROUP_CONCAT(DISTINCT tag.name) as matched_tags, 
                                GROUP_CONCAT(bookmark.created_at) as bookmark_time FROM article
                                JOIN bookmark 
                                ON article.id = bookmark.article_id
                                JOIN article_tags
                                ON article.id = article_tags.article_id
                                JOIN tag
                                ON article_tags.tag_id = tag.id
                                JOIN user_tag
                                ON tag.id = user_tag.tag_id
                                WHERE tag.name LIKE %s
                                AND user_tag.user_id = %s
                                AND bookmark.user_id = %s
                                GROUP BY article.id
                                ORDER BY article.published_at ASC""", [query_term, current_user_id, current_user_id])
            raw_article_data = cursor.fetchall()
        
    formatted_article_data = []
    for row in raw_article_data:
        article_dict = {
            "title": row[0],
            "link": row[1],
            "date": row[2],
            "tags": row[3],
        }
        formatted_article_data.append(article_dict)
        
    return JsonResponse({"articles": formatted_article_data})

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def bookmark_article(request):
    current_user_id = request.user.id
    payload = json.loads(request.body)
    target_article_id = payload.get('id')
    
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO bookmark (user_id, article_id, created_at) VALUES (%s, %s, CURRENT_TIMESTAMP)", [current_user_id, target_article_id])
                       
    return JsonResponse({"status": "success"})

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def remove_bookmark(request, id):
    current_user_id = request.user.id

    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM bookmark WHERE bookmark.user_id = %s and article_id = %s", [current_user_id, id])
    
    return JsonResponse({"status": "deleted"})  

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_tags(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT DISTINCT tag.id, tag.name FROM tag ORDER BY tag.name ASC")
        raw_tag_data=cursor.fetchall()
        formatted_tag_data = []
        for row in raw_tag_data:
            tag_dict = {
                "id": row[0],
                "name": row[1],
            }
            
            formatted_tag_data.append(tag_dict)
            
    return JsonResponse({"tags": formatted_tag_data})

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def set_user_tag(request):
    current_user_id = request.user.id
    payload = json.loads(request.body)
    target_tag_id = payload.get('id')
    
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO user_tag (user_id, tag_id, is_ignored, created_at) VALUES (%s, %s, False, CURRENT_TIMESTAMP)", [current_user_id, target_tag_id])
        
    return JsonResponse({"status": "success"})
        
        
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_tags(request):
    current_user_id = request.user.id
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT tag.id, tag.name from tag join user_tag on user_tag.tag_id = tag.id where user_tag.user_id = %s and user_tag.is_ignored = False", [current_user_id])
        
        raw_tag_data=cursor.fetchall()
        formatted_tag_data = []
        for row in raw_tag_data:
            tag_dict = {
                "id": row[0],
                "name": row[1],
            }
            
            formatted_tag_data.append(tag_dict)
            
    return JsonResponse({"tags": formatted_tag_data})
        
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def remove_user_tag(request, id):
    current_user_id = request.user.id
    
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM user_tag WHERE user_tag.user_id = %s and tag_id = %s", [current_user_id, id])
    
    return JsonResponse({"status": "deleted"})        

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_ignored_user_tags(request):
    current_user_id = request.user.id
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT tag.id, tag.name from tag join user_tag on user_tag.tag_id = tag.id where user_tag.user_id = %s and user_tag.is_ignored = True", [current_user_id])
        raw_tag_data=cursor.fetchall()
        formatted_tag_data = []
        for row in raw_tag_data:
            tag_dict = {
                "id": row[0],
                "name": row[1],
            }
            
            formatted_tag_data.append(tag_dict)
            
    return JsonResponse({"tags": formatted_tag_data})
        
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def set_ignored_user_tag(request):
    current_user_id = request.user.id
    payload = json.loads(request.body)
    target_tag_id = payload.get('id')
    
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO user_tag (user_id, tag_id, is_ignored, created_at) VALUES (%s, %s, True, CURRENT_TIMESTAMP)", [current_user_id, target_tag_id])
        
    return JsonResponse({"status": "success"})
        
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def remove_ignored_user_tag(request, id):
    current_user_id = request.user.id
    
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM user_tag WHERE user_tag.user_id = %s and tag_id = %s", [current_user_id, id])
    
    return JsonResponse({"status": "deleted"})

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_publications(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT DISTINCT publication.id, publication.name FROM publication")
        raw_pub_data=cursor.fetchall()
        formatted_pub_data = []
        for row in raw_pub_data:
            pub_dict = {
                "id": row[0],
                "name": row[1],
            }
            
            formatted_pub_data.append(pub_dict)
            
    return JsonResponse({"publications": formatted_pub_data})

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def set_user_publication(request):
    current_user_id = request.user.id
    payload = json.loads(request.body)
    target_pub_id = payload.get('id')
    
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO user_publication (user_id, publication_id, created_at) VALUES (%s, %s, CURRENT_TIMESTAMP)", [current_user_id, target_pub_id])
        
    return JsonResponse({"status": "success"})
        
        
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_publications(request):
    current_user_id = request.user.id
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT publication.id, publication.name from publication join user_publication on user_publication.publication_id = publication.id where user_publication.user_id = %s", [current_user_id])
        
        raw_pub_data=cursor.fetchall()
        formatted_pub_data = []
        for row in raw_pub_data:
            pub_dict = {
                "id": row[0],
                "name": row[1],
            }
            
            formatted_pub_data.append(pub_dict)
            
    return JsonResponse({"publications": formatted_pub_data})
        
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def remove_user_publication(request, id):
    current_user_id = request.user.id
    
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM user_publication WHERE user_publication.user_id = %s and publication_id = %s", [current_user_id, id])
    
    return JsonResponse({"status": "deleted"}) 