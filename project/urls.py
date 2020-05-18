"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
#from django.urls import path
from app import views
from django.conf.urls import url

urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^$', views.login_user, name='login'),
    url(r'^submit_register', views.submit_register, name='submit_register'),
    url(r'^recovery_pass', views.recovery_pass, name='recovery_pass'),
    url(r'^submit', views.submit_login, name='submit_login'),
    url(r'^index', views.index, name='index'),
    url(r'^logout', views.logout_user, name='logout'),
    url(r'^find', views.index, name='find'),

    #path("admin",admin.site.urls),
    #path("",views.login_user),
    #path("submit",views.submit_login),
    #path("submit_register",views.submit_register),
    #path("register",views.register),
    #path("recovery_pass",views.recovery_pass),
    #path("index.html",views.index),
    #path("/",views.logout_user)
]
