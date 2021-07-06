from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


phone_regex = RegexValidator(regex=r'^\+1?\d{9,15}$', message="Phone number must be entered in the format: '(+12)99999'. Up to 18 digits allowed.")
userOptions = (
    ("Client", "Client"),
    ("Developer", "Developer")
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
    ("Assignment", "Assignment"),
    ("Support","Support"),
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
    
   

    mobile = forms.CharField(validators=[phone_regex],
        widget=forms.TextInput(
            attrs={
                "placeholder":"Mobile Number with Country Code",
                "class":"form-control",
                "id":"mobile"
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

    College = forms.CharField(required=False,
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
