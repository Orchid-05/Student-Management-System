"""
URL configuration for SMS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

from studentapp.views import *


from django.conf import settings 
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('',home,name="home"),  
    path('home/',home,name="home"),  
    path('admin/', admin.site.urls),
    path('about/',about, name="about"),
    path('course/',AllCourse, name="AllCourse"),
    path('enroll/',enroll_course, name='enroll'),
    path('mycourse/',mycourse, name='mycourse'),
    path('profile/',profile, name='profile'),
    path('edit_profile/',edit_profile, name='edit_profile'),
    path('assignment/',assignment, name='assignment'),
    path('schedule/',schedule, name='schedule'),
    path('delete_course/<int:course_id>/', delete_course_ajax, name='delete_course_ajax'),
    path('contact', contact, name='contact'),



    path('admin_dashboard/', admin_dashboard , name='admin_dashboard'),
    path('admin/manage_users/',manage_users, name='admin_manage_users'),
    path('admin/logout/',admin_logout, name='admin_logout'),
    path('manage_users/',manage_users, name='manage_users'),
    path('edit_user/<int:user_id>/', edit_user, name='edit_user'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
    
    



    path('login/',login_page,name="login_page"),
    path('register/',register_page,name="register_page"),
    path('logout/',logout_page,name="logout_page"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()

