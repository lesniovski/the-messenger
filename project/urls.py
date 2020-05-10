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
    url(r'^submit', views.submit_login, name='submit_login'),
    url(r'^index', views.index, name='index'),
    url(r'^logout', views.logout_user, name='logout'),
    url(r'^register', views.register, name='register'),
    #url(r'^register_submit', views.register_submit, name='register_submit'),
    #url(r'^client/', views.client, name='client'),
    #path("",views.login_user),
    #path("submit",views.submit_login)
]
