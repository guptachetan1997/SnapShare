""" The URL routes for the posts app. """
from django.urls import path
from posts.views import Upload, SinglePost, LikeToggle, AddComment, SingleTag

urlpatterns = [
	path('upload/', Upload.as_view(), name="upload_url"),
	path('tags/<tag>/', SingleTag.as_view(), name="singletag_url"),
	path('single/like/', LikeToggle.as_view(), name="singlepostlike_url"),
	path('single/comment/', AddComment.as_view(), name="singlepostcomment_url"),
	path('single/<uuid>/', SinglePost.as_view(), name="singlepost_url")
]