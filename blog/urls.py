from django.urls import path ,re_path
from .views import (
    blog_post_create_view,
    blog_post_delete_view,
    blog_post_detail_page,
    blog_post_list_view,
    blog_post_update_view,
    profile_user,
    profiles,
    edit_profile,
    )

urlpatterns = [
	path('',blog_post_list_view),
    path('create/',blog_post_create_view),
    path('<int:post_id>/edit/',blog_post_update_view),
    path('<str:post_title>/<int:post_id>/edit/',blog_post_update_view),
    path('<int:post_id>/delete/',blog_post_delete_view),
    path('<str:post_title>/<int:post_id>/delete/',blog_post_delete_view),  
    path('<int:post_id>/',blog_post_detail_page),
    path('<str:post_title>/<int:post_id>/',blog_post_detail_page),
    path('profile/<str:user_name>/edit',edit_profile),
    path('profile/<str:user_name>/',profile_user),
    path('profiles',profiles),
    
]	
