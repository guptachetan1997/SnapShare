""" The URL routes for the posts app. """
from django.urls import path
from posts.views import Upload, SinglePost, LikeToggle

urlpatterns = [
	path('upload/', Upload.as_view(), name="upload_url"),
	path('single/like/', LikeToggle.as_view(), name="singlepostlike_url"),
	path('single/<uuid>/', SinglePost.as_view(), name="singlepost_url")
]