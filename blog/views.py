from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
import json
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Post, Comment

# Create your views here.

@csrf_exempt
def register(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)
    try:
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        if not username or not email or not password:
            return JsonResponse({'error': 'All fields required'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)
        user = User.objects.create_user(username=username, email=email, password=password)
        return JsonResponse({'message': 'User registered successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def login(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return JsonResponse({'message': 'Login successful'})
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def create_post(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    try:
        data = json.loads(request.body)
        title = data.get('title')
        content = data.get('content')
        if not title or not content:
            return JsonResponse({'error': 'Title and content required'}, status=400)
        post = Post.objects.create(author=request.user, title=title, content=content)
        return JsonResponse({'message': 'Post created', 'post_id': post.id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def posts_list(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET allowed'}, status=405)
    posts = Post.objects.all().order_by('-created_at')
    data = [
        {
            'id': post.id,
            'title': post.title,
            'author': post.author.username,
            'created_at': post.created_at,
        } for post in posts
    ]
    return JsonResponse({'posts': data})

def post_detail(request, id):
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET allowed'}, status=405)
    try:
        post = Post.objects.get(id=id)
        comments = [
            {
                'id': c.id,
                'user': c.user.username,
                'text': c.text,
                'created_at': c.created_at,
            } for c in post.comments.all().order_by('created_at')
        ]
        data = {
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'author': post.author.username,
            'created_at': post.created_at,
            'comments': comments,
        }
        return JsonResponse(data)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)

@csrf_exempt
def add_comment(request, id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    try:
        post = Post.objects.get(id=id)
        data = json.loads(request.body)
        text = data.get('text')
        if not text:
            return JsonResponse({'error': 'Text required'}, status=400)
        comment = Comment.objects.create(post=post, user=request.user, text=text)
        return JsonResponse({'message': 'Comment added', 'comment_id': comment.id})
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
