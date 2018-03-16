""" Views for the accounts app. """
from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login, logout, authenticate, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from accounts.forms import SignUpForm, ProfileUpdateForm, ProfilePictureUpdateForm
from django.contrib import messages
from accounts.models import Profile
from posts.models import Post

User = get_user_model()

class Login(View):
	template_name = "accounts/login.html"

	@method_decorator(csrf_protect)
	def get(self, request, *args, **kwargs):
		return render(request, self.template_name)
	
	@method_decorator(csrf_protect)
	def post(self, request, *args, **kwargs):
		username = request.POST.get("username")
		password = request.POST.get("password")
		try:
			user = User.objects.get(username=username)
			auth_user = authenticate(username = user.username, password = password)
			if auth_user is not None:
				login(request, user)
				return redirect("/accounts/profile/{}".format(user.username))
			else:
				messages.add_message(request, messages.ERROR, 'Incorrect Credentials')
				return redirect("/accounts/login/")	
		except Exception as e:
			messages.add_message(request, messages.ERROR, 'Incorrect Credentials')
			return redirect("/accounts/login/")

class Logout(View):
	
	@method_decorator(login_required)
	def get(self, request, *args, **kwargs):
		logout(request)
		return redirect("/accounts/login/")

class Register(View):
	template_name = "accounts/register.html"

	@method_decorator(csrf_protect)
	def get(self, request, *args, **kwargs):
		return render(request, self.template_name)

	@method_decorator(csrf_protect)
	def post(self, request, *args, **kwargs):
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.save()
			return redirect('/accounts/login/')
		else:
			errors = form.errors.get_json_data()
			for x in errors:
				for error in errors[x]:
					messages.add_message(request, messages.ERROR, error["message"])
			return redirect('/accounts/register/')


class Profile(View):
	template_name = "accounts/profile.html"

	@method_decorator(login_required)
	def get(self, request, username, *args, **kwargs):
		try:
			user = User.objects.get(username=username)
			if user:
				posts = user.profile.get_posts()
				following_flag = request.user.profile.check_connection(user)
			else:
				following_flag = None
				posts = None
		except Exception as e:
			print(e)
			user = None
		return render(request, self.template_name, {"user" : user, "following_flag" : following_flag, "posts" : posts})


class ProfileUpdate(View):
	
	@method_decorator(login_required, csrf_protect)
	def post(self, request, *args, **kwargs):
		form = ProfileUpdateForm(request.POST)
		if form.is_valid():
			if form.cleaned_data['first_name'] is not '':
				request.user.first_name=form.cleaned_data['first_name']
			if form.cleaned_data['last_name'] is not '':
				request.user.last_name=form.cleaned_data['last_name']
			if form.cleaned_data['bio'] is not '':
				request.user.profile.bio=form.cleaned_data['bio']
			if request.FILES:
				profile_picture_form = ProfilePictureUpdateForm(request.POST, request.FILES, instance=request.user.profile)
				if profile_picture_form.is_valid():
					profile_picture_form.save()
			request.user.save()
		else:
			errors = form.errors.get_json_data()
			for x in errors:
				for error in errors[x]:
					messages.add_message(request, messages.ERROR, error["message"])
		return redirect("/accounts/profile/{}".format(request.user.username))



class FollowToggle(View):

	@method_decorator(login_required, csrf_protect)
	def post(self, request, *args, **kwargs):
		to_user = request.POST.get("to_user")
		data = request.user.profile.toggle_connection(to_user)
		if data["status"]:
			return JsonResponse({"success" : True, "following_flag" : data["following_flag"]})
		else:
			return JsonResponse({"success" : False})

@login_required
def temp_home(request):
	return redirect("/accounts/profile/{}".format(request.user.username))


@login_required
def four_o_four(request):
	return render(request, "SnapShare/404.html")