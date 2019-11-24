"""try_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path ,re_path , include

from .views import (
	home_page,
	about_page,
    contact_page,
    sign_up,
    login_user,
    logout_user,
	)

from search.views import search_view
from blog.views import (
    task_view,          
    task_create,        
    task_detail,
    task_edit,
    task_delete,

    project_view,
    project_create,
    project_detail,
    project_edit,
    project_delete,

    diary_view,
    diary_detail,
    diary_create,
    diary_update,
    diary_delete)

urlpatterns = [
	path('', home_page),
    path('blog/',include('blog.urls')),
    #path('search/',include('blog.urls')),
    path('search/',search_view),
	re_path(r'^pages?/$', about_page),
	re_path(r'^about/$', about_page),
    path('contact/',contact_page),
    path('admin/', admin.site.urls),
    path('signup/',sign_up),
    path('login/',login_user),
    path('logout/',logout_user),

    path('tasks/',task_view),
    path('tasks/create',task_create),
    path('tasks/<str:task_name>/<int:task_id>/',task_detail),
    path('tasks/<str:task_name>/<int:task_id>/<str:save>',task_detail),
    path('tasks/<str:task_name>/<int:task_id>/edit/', task_edit),
    path('tasks/<str:task_name>/<int:task_id>/delete/', task_delete),

    path('projects/',project_view),
    path('projects/create',project_create),
    path('projects/<str:project_name>/<int:project_id>/',project_detail),
    path('projects/<str:project_name>/<int:project_id>/edit/',project_edit),
    path('projects/<str:project_name>/<int:project_id>/delete/',project_delete),

    path('diaries/',diary_view),
    path('diaries/create',diary_create),
    path('diaries/<str:diary_title>/<int:diary_id>/',diary_detail),
    path('diaries/<str:diary_title>/<int:diary_id>/edit/',diary_update),
    path('diaries/<str:diary_title>/<int:diary_id>/delete/',diary_delete),
]



if settings.DEBUG:
    #test mode i.e. debug is still true
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)