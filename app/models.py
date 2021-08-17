from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
# Create your models here.
phone_regex = RegexValidator(regex=r'^\+1?\d{9,15}$', message="Phone number must be entered in the format: '+(country Code)99999'. Up to 18 digits allowed.")

class userType(models.Model):
    UserChoice = [
        ("Developer","Developer"),
        ("Client","Client")
    ]
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    userType = models.CharField(max_length=20,default="",choices=UserChoice)

    def __str__(self):
        return self.user.username

class Client(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    mobile = models.CharField(validators=[phone_regex],max_length=18)
    Description = models.CharField(default="",max_length=150)
    projectChoice = [
        ("Enterprise Projects","Enterprise Projects"),
        ("Academic Task","Academic Task"),
        ("Job Support","Job Support"),
        ("Others","Others")
    ]
    ProjectType = models.CharField(default="",choices=projectChoice,max_length=40)
    CollegeName = models.CharField(max_length=40,null=True,blank=True)


    def __str__(self):
        return self.user.username

class Developer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    skillChoice = [
        ("Web Development","Web Development"),
        ("Android Development","Android Development"),
        ("Artificial Intelligence","Artificial Intelligence"),
        ("Machine Learning","Machine Learning"),
        ("Data Sceince","Data Science"),
        ("Others","Others")
    ]
    Skills = models.CharField(default="",max_length=120)
    Description = models.CharField(default="",max_length=150)
    mobile = models.CharField(validators=[phone_regex],max_length=18)


    def __str__(self):
        return self.user.username


class Project(models.Model):
    user = models.ForeignKey(Client,on_delete=models.CASCADE)
    percentage = [
        ("25%","25%"),
        ("50%","50%"),
        ("75%","75%"),
        ("100%","100%")
    ]
    status = [
        ("Pending","Pending"),
        ("Accepted","Accepted"),
        ("Assigned","Assigned"),
        ("Delievred","Delievred"),
        ("Completed","Completed"),
        ("Rejected","Rejected")
    ]
    currency = [
        ("EURO","EURO"),
        ("USD","USD"),
        ("AUD","AUD"),
        ("SGP","SGP"),
        ("GBP","GBP")
    ]
    payment = [
       ("Not Paid","Not Paid"),
       ("Partially Paid","Partially Paid"),
       ("Fully Paid","Fully Paid")
    ]
    type = [
        ("Dissertation","Dissertation"),
        ("Assignment","Assignment"),
        ("Technical Report","Technical Report"),
        ("Others","Others")
    ]
    Title = models.CharField(max_length=50)
    Date = models.DateField(default=timezone.now)
    ActualPrice = models.IntegerField(blank=True,default=0)
    CoderPrice = models.IntegerField(blank=True,default=0)
    Description = models.CharField(max_length=200,default="")
    currencyCode = models.CharField(max_length=15,choices=currency,blank=True)
    ClientDeadline = models.DateField(blank=True,null=True)
    Status = models.CharField(max_length=40,choices = status,default="Pending")
    PaymentStatus = models.CharField(max_length=40,choices=payment,default="Not Paid")
    projectType = models.CharField(max_length=30,choices= type,default="")
    SentTO = models.ManyToManyField(Developer,blank=True)
    CompletePercentage = models.CharField(max_length=25,blank=True,choices=percentage,default=0)
    feedback = models.CharField(max_length=150,null=True,blank=True)
    ClientDiscussion = models.CharField(max_length=250,null=True,blank=True)
    DeveloperDiscussion = models.CharField(max_length=250,blank=True,null=True)

    def __str__(self):
        return self.Title

class Bid(models.Model):
    currency = [
        ("EURO","EURO"),
        ("USD","USD"),
        ("AUD","AUD"),
        ("SGP","SGP"),
        ("GBP","GBP")
    ]
    userName = models.ForeignKey(Developer,on_delete=models.CASCADE)
    projectName = models.ForeignKey(Project,on_delete=models.CASCADE)
    currencyCode = models.CharField(max_length=15,choices=currency,blank=True)
    bidAmount = models.IntegerField(default=0)

    class Meta:
        unique_together = [["userName","projectName"]]

    def __str__(self):
        return self.userName.user.username


class File(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    files = models.FileField(blank=True,upload_to="projects")
    Verified = models.BooleanField(blank=True,null=True)
    fileName = models.CharField(max_length=100,blank=True)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.project.Title


class Payment(models.Model):
    currency = [
        ("EURO","EURO"),
        ("USD","USD"),
        ("AUD","AUD"),
        ("SGP","SGP"),
        ("GBP","GBP")
    ]
    projectName = models.ForeignKey(Project,null=True,on_delete=models.CASCADE)
    Amount = models.IntegerField(default=0)
    Date = models.DateField(default=timezone.now)
    currencyCode = models.CharField(max_length=15,choices=currency,blank=True)

    def __str__(self):
        return self.projectName.Title


class Assign(models.Model):
    currency = [
        ("EURO","EURO"),
        ("USD","USD"),
        ("AUD","AUD"),
        ("SGP","SGP"),
        ("GBP","GBP")
    ]
    DeveloperDeadline = models.DateField(blank=True,null=True)
    userName = models.ForeignKey(Developer,on_delete=models.CASCADE)
    projectName = models.ForeignKey(Project,on_delete=models.CASCADE)
    Amount= models.IntegerField(default=0)
    Date = models.DateField(default=timezone.now)
    currencyCode = models.CharField(max_length=15,choices=currency,blank=True)

    class Meta:
        unique_together = [["userName","projectName"]]


    def __str__(self):
        return self.projectName.Title
