from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
import json
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from .models import Post, Comment, Like

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
    
    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 10)  # 10 posts per page
    
    try:
        posts_page = paginator.page(page)
    except:
        posts_page = paginator.page(1)
    
    data = [
        {
            'id': post.id,
            'title': post.title,
            'author': post.author.username,
            'created_at': post.created_at,
            'like_count': post.like_count(),
        } for post in posts_page
    ]
    
    return JsonResponse({
        'posts': data,
        'pagination': {
            'current_page': posts_page.number,
            'total_pages': paginator.num_pages,
            'has_next': posts_page.has_next(),
            'has_previous': posts_page.has_previous(),
        }
    })

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
            'like_count': post.like_count(),
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

@csrf_exempt
def edit_post(request, id):
    if request.method != 'PUT':
        return JsonResponse({'error': 'Only PUT allowed'}, status=405)
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    try:
        post = get_object_or_404(Post, id=id)
        if post.author != request.user:
            return JsonResponse({'error': 'Permission denied'}, status=403)
        
        data = json.loads(request.body)
        title = data.get('title')
        content = data.get('content')
        
        if title:
            post.title = title
        if content:
            post.content = content
        
        post.save()
        return JsonResponse({'message': 'Post updated successfully'})
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def delete_post(request, id):
    if request.method != 'DELETE':
        return JsonResponse({'error': 'Only DELETE allowed'}, status=405)
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    try:
        post = get_object_or_404(Post, id=id)
        if post.author != request.user:
            return JsonResponse({'error': 'Permission denied'}, status=403)
        
        post.delete()
        return JsonResponse({'message': 'Post deleted successfully'})
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def edit_comment(request, id):
    if request.method != 'PUT':
        return JsonResponse({'error': 'Only PUT allowed'}, status=405)
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    try:
        comment = get_object_or_404(Comment, id=id)
        if comment.user != request.user:
            return JsonResponse({'error': 'Permission denied'}, status=403)
        
        data = json.loads(request.body)
        text = data.get('text')
        
        if text:
            comment.text = text
            comment.save()
            return JsonResponse({'message': 'Comment updated successfully'})
        else:
            return JsonResponse({'error': 'Text required'}, status=400)
    except Comment.DoesNotExist:
        return JsonResponse({'error': 'Comment not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def delete_comment(request, id):
    if request.method != 'DELETE':
        return JsonResponse({'error': 'Only DELETE allowed'}, status=405)
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    try:
        comment = get_object_or_404(Comment, id=id)
        if comment.user != request.user:
            return JsonResponse({'error': 'Permission denied'}, status=403)
        
        comment.delete()
        return JsonResponse({'message': 'Comment deleted successfully'})
    except Comment.DoesNotExist:
        return JsonResponse({'error': 'Comment not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def like_post(request, id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    try:
        post = get_object_or_404(Post, id=id)
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        
        if created:
            return JsonResponse({'message': 'Post liked', 'liked': True})
        else:
            return JsonResponse({'message': 'Post already liked', 'liked': True})
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def unlike_post(request, id):
    if request.method != 'DELETE':
        return JsonResponse({'error': 'Only DELETE allowed'}, status=405)
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    try:
        post = get_object_or_404(Post, id=id)
        like = get_object_or_404(Like, post=post, user=request.user)
        like.delete()
        return JsonResponse({'message': 'Post unliked', 'liked': False})
    except (Post.DoesNotExist, Like.DoesNotExist):
        return JsonResponse({'error': 'Post or like not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
