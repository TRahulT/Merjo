from django.urls import path
from .views import create_blog_post, create_comment, list_blog_posts, list_comments, update_blog_post,authenticated_api

urlpatterns = [
    path('posts/', list_blog_posts, name='list-blog-posts'),
    path('posts/<int:post_id>/comments/', list_comments, name='list-comments'),
    path('posts/<int:post_id>/comments/create/', create_comment, name='create-comment'),
    path('posts/create/', create_blog_post, name='create-blog-post'),
    path('posts/<int:post_id>/update/', update_blog_post, name='update-blog-post'),
    path('test/', authenticated_api,name='test'),
]
