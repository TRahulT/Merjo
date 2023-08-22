# Merjo


topic: Installation: 
1. install django 
command: pip install django

2. install pyjwt
command : pip install pyjwt

3. start project Merjo_blog (Project Name)
command: django admin start project Merjo_blog

4. install two apps:
i) python manage.py blog
ii) python manage.py users

5. mention these dependencies in the 'settings.py' file

6. create a User in 'users' app
('User' will be created by inheriting the abstract user)

7. Inside 'blog' app, create following tables: 'comments', 'posts'

MAIN: 

For this project, following are mendatory:
1. JWT for encryption and decription
2. Encryption is done in 'views.py' of 'users' app while login.
code :
@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            payload = {
                'user_id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
            }
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

            return JsonResponse({'token': token, 'loggedin': 'successfully', 'username': username})
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)


3. We have to create a middleware to handle the token: 
code:
import jwt
from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse


class TokenAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == reverse('login'):
            return self.get_response(request)
        if request.path == reverse('register'):
            return self.get_response(request)

        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[-1]

        if not token:
            return JsonResponse({'error': 'Token missing'}, status=401)

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            request.user_id = payload['user_id']
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'Token expired'}, status=401)
        except jwt.DecodeError:
            return JsonResponse({'error': 'Token invalid'}, status=401)

        return self.get_response(request)
4. Code:
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

>> API Testing using 'POSTMAN": 
Set headers: Content-Type : multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW
