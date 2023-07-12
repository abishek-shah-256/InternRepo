from . import views
from django.urls import path, include
from .views import ProfileListView, ProfileDetailView

app_name = "profiles"

urlpatterns = [
    path('myprofile/', views.myProfile, name="myProfile"),
    path('editprofile/<int:pk>/', views.editProfile, name="editProfile"),
   
    path('listprofile', ProfileListView.as_view(), name='profile-list-view'),
    path('otherprofile/<pk>/', ProfileDetailView.as_view(), name='profile-detail-view'),
    path('switch_friend/', views.friend_unfriend_profile, name='friend-unfriend-profile')
]