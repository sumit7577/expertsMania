from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.db.models.fields import BinaryField


phone_regex = RegexValidator(regex=r'^\+1?\d{9,15}$', message="Phone number must be entered in the format: '(+12)99999'. Up to 18 digits allowed.")
userOptions = (
    ("Client", "Client"),
    ("Developer", "Developer")
)


def customMobileValidator(mobile):
    print(mobile)
    UserData = User.objects.all()
    for i in UserData:
        if(not i.is_superuser):
            try:
                if(i.developer.mobile == mobile):
                    raise forms.ValidationError("Mobile Number already Exists")

            except:
                print("fuck")


Skills = (
    ("Android Development", "Android Development"),
    ("Web Development", "Web Development"),
    ("Machine Learning", "Machine Learning"),
    ("Data Science", "Data Science"),
    ("Artificial Intelligence", "Artificial Intelligence"),
    ("Others","Others")
)

Project = (
    ("Enterprise Projects", "Enterprise Projects"),
    ("Academic Task", "Academic Task"),
    ("Job Support","Job Support"),
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


    Skills = forms.MultipleChoiceField(choices=Skills,required=False,
        widget=forms.SelectMultiple(
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
    
   

    mobile = forms.CharField(validators=[phone_regex,customMobileValidator],
        widget=forms.TextInput(
            attrs={
                "placeholder":"Mobile Number with Country Code ex(+1)9999",
                "class":"form-control",
                "id":"mobile"
            }
        ))

    def mobileCheck(self):
        mobilenumber = self.cleaned_data.get("mobile")
        customMobileValidator(mobilenumber)

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
