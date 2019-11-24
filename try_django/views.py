from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from blog.forms import UserCreateForm
from django.contrib.auth.decorators import login_required
from .forms import ContactForm, LoginUser

def home_page(request):
	my_title="Stablr"
	context = {"title" : my_title}
	return render(request, "home.html", context)

def about_page(request):
	context={"title" : "About Us"}
	return render(request,"about.html",context)

def contact_page(request):
	form = ContactForm(request.POST or None)
	if form.is_valid():
		print(form.cleaned_data)

	context={
		"title" : "Contact Us",
		"form"  : form
 	}
	return render(request, "form.html",context)	

def sign_up(request):
	if not request.user.is_authenticated:
		form = UserCreateForm(request.POST or None)
		if request.method == 'POST':
			if form.is_valid():
				form.save()
				username=form.cleaned_data.get('username')
				raw_password = form.cleaned_data.get('password1')
				user = authenticate(username=username,password=raw_password)
				login(request,user)
				return render(request,'home.html')

		return render(request,'signup.html',{'form':form})
	else:
		return redirect('/blog/')		

def login_user(request):
	if not request.user.is_authenticated:
		form = LoginUser(request.POST or None)
		if form.is_valid():
			username=form.cleaned_data.get('username')
			password=form.cleaned_data.get('password')
			user = authenticate(username=username,password=password)
			login(request,user)
			return render(request,'home.html')

		return render(request,'login.html',{'form':form})
	else:
		return redirect('/blog/')		

@login_required
def logout_user(request):
	if request.user.is_authenticated:
		logout(request)
		return redirect('/')

