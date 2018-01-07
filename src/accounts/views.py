""" Views for the accounts app. """
from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login, logout, authenticate, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from accounts.forms import SignUpForm
from django.contrib import messages

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
				return redirect("/")
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
		return redirect("/")

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