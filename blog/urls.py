from django.urls import path
from . import views

urlpatterns = [
    path('api/register/', views.register, name='register'),
    path('api/login/', views.login, name='login'),
    path('api/create-post/', views.create_post, name='create_post'),
    path('api/posts/', views.posts_list, name='posts_list'),
    path('api/post/<int:id>/', views.post_detail, name='post_detail'),
    path('api/post/<int:id>/comment/', views.add_comment, name='add_comment'),
    path('api/post/<int:id>/edit/', views.edit_post, name='edit_post'),
    path('api/post/<int:id>/delete/', views.delete_post, name='delete_post'),
    path('api/comment/<int:id>/edit/', views.edit_comment, name='edit_comment'),
    path('api/comment/<int:id>/delete/', views.delete_comment, name='delete_comment'),
    path('api/post/<int:id>/like/', views.like_post, name='like_post'),
    path('api/post/<int:id>/unlike/', views.unlike_post, name='unlike_post'),
] 