from django.urls import path
from . import views

urlpatterns = [
    path('api/register/', views.register, name='register'),
    path('api/login/', views.login, name='login'),
    path('api/create-post/', views.create_post, name='create_post'),
    path('api/posts/', views.posts_list, name='posts_list'),
    path('api/post/<int:id>/', views.post_detail, name='post_detail'),
    path('api/post/<int:id>/comment/', views.add_comment, name='add_comment'),
] 