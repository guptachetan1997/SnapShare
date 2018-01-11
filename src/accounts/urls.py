""" The URL routes for the accounts app. """
from django.urls import path
from accounts.views import Login, Logout , Register, Profile, FollowToggle, ProfileUpdate

urlpatterns = [
	path('login/', Login.as_view(), name="login_url"),
	path('logout/', Logout.as_view(), name="logout_url"),
	path('register/', Register.as_view(), name="register_url"),
	path('profile/<str:username>/update/', ProfileUpdate.as_view(), name="profile_edit_url"),
	path('profile/<str:username>/', Profile.as_view(), name="profile_url"),
	path('followtoggle/', FollowToggle.as_view(), name="follow_url"),
]