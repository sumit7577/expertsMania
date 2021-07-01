from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm
from app.models import Client,Developer,userType
from django.contrib.auth.decorators import login_required

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
            user = authenticate(username=username, password=raw_password)
            userType.objects.update_or_create(user=user,userType=usertype)

            msg     = 'User created - please <a href="/login">login</a>.'
            success = True
            
            return redirect("/profile/")

        else:
            msg = 'Form is not valid'    
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg" : msg, "success" : success })


@login_required(login_url="/login")
def profile(request):
    message = None
    Success = False
    if request.method == "POST":
        if request.user.usertype.userType == "Developer":
            mobile = request.POST.get("number")
            skills = request.POST.get("skills")
            desc = request.POST.get("desc")
            
            try:
                user = Developer(user=request.user, mobile=mobile,
                            Skills=skills, Description=desc)
                user.save()
                message = "Profile Successfully Updated"
                Success = True
                return redirect("/")
            except:
                message = "Please fill up the form Correctly"
                Success = False
            
            
        elif(request.user.usertype.userType == "Client"):
            mobile = request.POST.get("number")
            project = request.POST.get("ptype")
            desc = request.POST.get("desc")
            try:
                data = Client(user=request.user, mobile=mobile,
                        ProjectType=project, Description=desc)
                data.save()
                message = "Profile Successfully Updated"
                Success = True
                return redirect("/")
            except:
                message = "Please fill up the form Correctly"
                Success = False
            
    return render(request,"complete.html",{"data":message,"success":Success})
