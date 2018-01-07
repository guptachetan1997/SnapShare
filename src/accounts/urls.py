""" The URL routes for the accounts app. """
from django.urls import path
from accounts.views import Login, Logout , Register

urlpatterns = [
	path('login/', Login.as_view(), name="login_url"),
	path('logout/', Logout.as_view(), name="logout_url"),
	path('register/', Register.as_view(), name="register_url"),
]