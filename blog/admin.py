from django.contrib import admin
from .models import Comment,BlogPost

# Register your models here.
admin.site.register(Comment)
admin.site.register(BlogPost)
