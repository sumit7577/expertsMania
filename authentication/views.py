from re import L
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm
from app.models import Client,Developer,userType
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:    
                msg = 'Invalid credentials'    
        else:
            msg = 'Error validating the form'    

    return render(request, "accounts/login.html", {"form": form, "msg" : msg})

def register_user(request):

    msg     = None
    success = False
    
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            usertype = form.cleaned_data.get("userType")
            skills = form.cleaned_data.get("Skills")
            projectType = form.cleaned_data.get("ProjectType")
            mobile = form.cleaned_data.get("mobile")
            desc = form.cleaned_data.get("Description")
            collegeName = form.cleaned_data.get("College")
            user = authenticate(username=username, password=raw_password)
            userType.objects.update_or_create(user=user,userType=usertype)
            if usertype == "Developer":
                Developer.objects.update_or_create(user=user,mobile=mobile,Skills=skills,Description=desc)
            else:
                Client.objects.update_or_create(user=user,ProjectType=projectType,mobile=mobile,Description=desc,CollegeName=collegeName)

            msg     = 'User created - please <a href="/login">Please Login to your Account</a>.'
            success = True

        else:
            msg = 'Form is not valid'    
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg" : msg, "success" : success })
