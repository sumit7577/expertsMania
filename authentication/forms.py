from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


userOptions = (
    ("Developer", "Developer"),
    ("Client", "Client")
)

Skills = (
    ("Android Development", "Android Development"),
    ("Web Development", "Web Development"),
    ("Machine Learning", "Machine Learning"),
    ("Data Science", "Data Science"),
    ("Artificial Intelligence", "Artificial Intelligence")
)

Project = (
    ("Production Projects", "Production Projects"),
    ("College Projects", "College Projects"),
    ("Others", "Others")
)


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password check",
                "class": "form-control"
            }
        ))

    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "First Name",
                "class": "form-control"
            }
        ))

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Last Name",
                "class": "form-control"
            }
        ))

    userType = forms.ChoiceField(choices=userOptions,
        widget=forms.Select(
            attrs={
                "placeholder":"User Type",
                "class":"form-control",
                "id":"userType"
            }
        ))

    Skills = forms.ChoiceField(choices=Skills,
        widget=forms.Select(
            attrs={
                "class":"form-control",
                "id":"skills"
            }
        ))
    
    ProjectType = forms.ChoiceField(choices=Project,
        widget=forms.Select(
            attrs={
                "class":"form-control",
                "id":"projectType"
            }
        ))
    phone = RegexValidator(regex=r'^\+?1?\d{9,15}$',message="Phone number must be starting with country Code and :+91 and must be less than 15 digit")
    mobile = forms.IntegerField(validators=[phone],
        widget=forms.NumberInput(
            attrs={
                "id":"mobile",
                "class": "form-control",
                "placeholder":"Mobile Number"
            }
        ))

    Description = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "id":"desc",
                "class": "form-control",
                "placeholder":"Tell About yourself and your work"
            }
        ))

    College = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "id":"Cname",
                "class": "form-control",
                "placeholder":"Please Enter Your College Name"
            }
        ))


    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2','first_name','last_name','userType','Skills','Description','mobile','ProjectType')
