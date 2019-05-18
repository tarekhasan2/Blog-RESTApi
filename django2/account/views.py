from django.shortcuts import render

# Create your views here.
from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout,
	)

from django.shortcuts import render, redirect, reverse
from .form import UserLoginForm, UserRegisterForm

def login_view(request):
	title = "Login"
	next = request.GET.get('next')
	form = UserLoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user = authenticate(username=username, password=password)
		#user.is_staff = True
		login(request, user)
		if next:
			return redirect(next)
		return redirect('/posts')


	context = {
		"title":title,
		"form" : form

	}
	return render(request, "login_view.html",context)


def register_view(request):
	title = "Register"
	next = request.GET.get('next')
	form = UserRegisterForm(request.POST or None)
	if form.is_valid():
		user = form.save(commit=False)
		password = form.cleaned_data.get("password")
		user.set_password(password)
		user.is_staff = True
		user.save()
		if next:
			return redirect(next)
		return redirect('/account')
		#new_user = authenticate(username=user.username, password=password)
		#login(request, new_user)

	context = {
		"title":title,
		"form" : form
	
	}
	return render(request, "login_view.html",context)

def logout_view(request):
	logout(request)

	context = {
	
	}
	return render(request, "login_view.html",context)