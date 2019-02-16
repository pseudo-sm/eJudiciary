"""eJudiciary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^advocate',views.advocate,name="advocate"),
    url(r'^judge',views.judge,name="judge"),
    url(r'^filefir',views.filefir,name="filefir"),
    url(r'^profile',views.profile,name="profile"),
    url(r'^police',views.police_home,name="police"),
    url(r'^logout',views.logout,name="logout"),
    url(r'^signup',views.signup,name="signup"),
    url(r'^login',views.login,name="login"),
    url(r'^home',views.home,name="home"),
    url(r'^auth-signup',views.auth_signup,name="auth_signup"),
    url(r'',views.index,name="index"),
]
