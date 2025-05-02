"""
URL configuration for simplelms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from core.views import index, testing, all_courses, course_statistics, user_profile

urlpatterns = [
    path('admin/', admin.site.urls),
    path('testing/', testing, name='testing'),
    path('courses/', all_courses, name='all_courses'),
    path('course-statistics/', course_statistics, name='course_statistics'),
    path('profile/<int:user_id>/', user_profile, name='user_profile'),
    path('', index, name='home'),
    path('silk/', include('silk.urls', namespace='silk')),
]