from . import views
from django.urls import path, include
from .views import ProfileListView, ProfileDetailView

app_name = "profiles"

urlpatterns = [
    path('myprofile/', views.myProfile, name="myProfile"),
    path('editprofile/<int:pk>/', views.editProfile, name="editProfile"),
   
    path('listprofile', ProfileListView.as_view(), name='profile-list-view'),
    path('otherprofile/<pk>/', ProfileDetailView.as_view(), name='profile-detail-view'),
    path('unfriend_friend/', views.unfriend_profile, name='unfriend-profile'),

#    ------new logic of add friend
    path('my_invites/',views.invites_received_view, name='my-invites-view'),

    path('send_friend_request/',views.send_request, name='send-request'),
    path('accept_friend_request/<pk>/',views.accept_friend_request, name='accept-request'),
    path('reject_friend_request/<pk>/',views.reject_friend_request, name='reject-request'),
    

]