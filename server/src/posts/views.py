from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from posts.models import Post, Comment
from posts.forms import PostForm
from accounts.models import Connection
from django.conf import settings
import requests
import io
import json
from PIL import Image

User = get_user_model()


# Create your views here.
class Upload(View):
	template_name = "posts/upload.html"

	@method_decorator(csrf_protect,login_required)
	def get(self, request, *args, **kwargs):
		return render(request, self.template_name)
	
	@method_decorator(csrf_protect, login_required)
	def post(self ,request, *args, **kwargs):
		form = PostForm(request.POST, request.FILES)
		if form.is_valid():
			post_obj = form.save(commit=False)
			post_obj.user = request.user
			post_obj.save()
			#sending request to the model server
			image_path = "{}/{}".format(settings.MEDIA_ROOT,post_obj.image)
			image = open(image_path, "rb").read()
			payload = {"image": image}
			r = requests.post(settings.TAGGER_SERVICE_URL, files=payload).json()
			if r["success"]:
				post_obj.tags = ",".join(r["tags"])
				post_obj.save()
			else:
				print("Error")
			return redirect("/accounts/profile/{}".format(request.user.username))
		else:
			errors = form.errors.get_json_data()
			print(errors)
			for x in errors:
				for error in errors[x]:
					messages.add_message(request, messages.ERROR, error["message"])
			return redirect("/posts/upload/")


class SinglePost(View):
	template_name = "posts/single.html"

	@method_decorator(csrf_protect, login_required)
	def get(self, request, uuid, *args, **kwargs):
		try:
			post_obj = Post.objects.get(uuid = uuid)
			like_flag = post_obj.check_like(request.user)
			comments = Comment.objects.filter(post=post_obj).order_by("-timestamp")
			tags = post_obj.tags.split(",")
			return render(request, self.template_name, {"post" : post_obj, "like_flag" : like_flag, "comments" : comments, "tags" : tags})
		except Exception as e:
			return redirect("/404/")


class LikeToggle(View):

	@method_decorator(login_required, csrf_protect)
	def post(self, request, *args, **kwargs):
		try:
			post_uuid = request.POST.get("post_uuid")
			post_obj = Post.objects.get(uuid = post_uuid)
			data = post_obj.toggle_like(request.user)
			if data["status"]:
				return JsonResponse({"success" : True, "like_flag" : data["like_flag"]})
			else:
				return JsonResponse({"success" : False})
		except Exception as e:
			print(e)
			return redirect("/404/")


class HomeView(View):
	template_name = "posts/home.html"

	@method_decorator(login_required)
	def get(self, request, *args, **kwargs):
		connections = Connection.objects.filter(from_user = request.user)
		posts = []
		for connection in connections:
			posts += Post.objects.filter(user=connection.to_user)
		return render(request, self.template_name, {"posts" : posts})


class AddComment(View):

	@method_decorator(login_required, csrf_protect)
	def post(self, request, *args, **kwargs):
		post_uuid = request.POST.get("post_uuid")
		text = request.POST.get("comment_text")
		try:
			post_obj = Post.objects.get(uuid = post_uuid)
			comment_create_flag = post_obj.add_comment(request.user, text)
			return redirect("/posts/single/{}/".format(post_obj.uuid))
		except:
			return redirect("/posts/single/{}/".format(post_obj.uuid))
