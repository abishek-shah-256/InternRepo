from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt


# app_name = "app1"

urlpatterns = [
    path('authenticate/<token>/',views.authenticatee,name="authenticatee"),
    path('', views.signin, name="signin"),
    path('signup', views.signup, name="signup"),
    path('home', views.home, name="home"),
    path('logout', views.logoutt, name="logout"),
    path('getpost', views.getupdatedPost, name="getpost"),
    
    path('handlecomment', views.handleComment, name="handleComment"),
    path('handlelike/<int:pid>', views.handleLike, name="handleLike"),
    path('search', csrf_exempt(views.search), name="search"),


]

