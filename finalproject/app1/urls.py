from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

# app_name = "app1"

urlpatterns = [
    path('home', views.home, name="home"),
    path('', views.signin, name="signin"),
    path('signup', views.signup, name="signup"),
    path('logout', views.logout, name="logout"),
    path('messenger', views.messenger, name="messenger"),
    path('userprofile', views.userprofile, name="userprofile"),
    path('getpost', views.getupdatedPost, name="getpost"),
    
    path('handlecomment', views.handleComment, name="handleComment"),
    

]

