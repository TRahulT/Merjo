# In project/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),  # Include user authentication URLs
    path('', include('blog.urls')),     # Include blog app's API URLs
]
