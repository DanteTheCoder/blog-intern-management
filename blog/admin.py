from django.contrib import admin

# Register your models here.

from .models import BlogPost,UserProfile,Tasks,Project


admin.site.register(BlogPost)
admin.site.register(UserProfile)
admin.site.register(Tasks)
admin.site.register(Project)