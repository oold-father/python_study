"""web_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from web01 import views

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'', views.index,name='index'),
    path(r'home/', views.home,name='home'),
    path(r'register/', views.register,name='register'),
    path(r'login/', views.login,name='login'),
    path(r'logout/', views.logout,name='logout'),
    path(r'learn/', views.learn,name='learn'),
    path(r'note/', views.note,name='note'),
    path(r'note/<id>/',views.noteinfo, name='noteinfo'),
    path(r'problem/', views.problem,name='problem'),
    path(r'problem/<int:id>/', views.probleminfo,name='probleminfo'),
    path(r'total/', views.total,name='total'),
    path(r'learn/<int:id>/', views.learninfo,name='learninfo'),
]

