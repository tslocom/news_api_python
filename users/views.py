import json
from django.shortcuts import render
from django.db import connection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# Create your views here.
@csrf_exempt
def create_user(request):
    payload = json.loads(request.body)
    username = payload.get('username')
    password = payload.get('password')
    
    new_user = User.objects.create_user(username=username, password=password)
    new_token = Token.objects.create(user=new_user)
                       
    return JsonResponse({'token': new_token.key})

@csrf_exempt
def login_user(request):
    payload = json.loads(request.body)
    username = payload.get('username')
    password = payload.get('password')
    user = authenticate(username=username, password=password)
    if user == None:
        return JsonResponse({'error': 'Invalid credentials'},
                            status=400)
    else:
        token, created = Token.objects.get_or_create(user=user)
        return JsonResponse({'token': token.key})