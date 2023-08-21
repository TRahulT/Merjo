from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import BlogPost, Comment
from .serializers import BlogPostSerializer, CommentSerializer
from .middleware import TokenAuthenticationMiddleware


@api_view(['POST'])
def create_blog_post(request):
    user_id = getattr(request, 'user_id', None)
    if user_id is not None:
        serializer = BlogPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author_id=user_id)
            return Response(serializer.data )
        return Response(serializer.errors )
    return Response({'error': 'Unauthorized'})


@api_view(['POST'])
def create_comment(request, post_id):
    user_id = getattr(request, 'user_id', None)
    if user_id is not None:
        post = BlogPost.objects.get(pk=post_id)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    else:
        return Response({'error': 'Unauthorized'}, status=401)

@api_view(['GET'])
def list_blog_posts(request):
    posts = BlogPost.objects.all()
    serializer = BlogPostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def list_comments(request, post_id):
    comments = Comment.objects.filter(post=post_id)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
def update_blog_post(request, post_id):
    user_id = getattr(request, 'user_id', None)
    if user_id is not None:
        post = BlogPost.objects.get(pk=post_id)
        if request.user == post.author:
            serializer = BlogPostSerializer(instance=post, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        return Response({'error': 'You do not have permission to update this post'}, status=403)
    else:
        return Response({'error': 'Unauthorized'}, status=401)


@api_view(['GET'])

def authenticated_api(request):
    user_id = getattr(request, 'user_id', None)

    if user_id is not None:
        return Response({'message': 'Authenticated API accessed', 'user_id': user_id})
    else:
        return Response({'error': 'Unauthorized'}, status=401)
