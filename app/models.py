
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

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
    mobile = models.IntegerField(default=0)
    Description = models.CharField(default="",max_length=150)
    projectChoice = [
        ("Production Projects","Production Projects"),
        ("College Projects","College Projects"),
        ("Others","Others")
    ]
    ProjectType = models.CharField(default="",choices=projectChoice,max_length=40)


    def __str__(self):
        return self.user.username

class Developer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    skillChoice = [
        ("Web Development","Web Development"),
        ("Android Development","Android Development"),
        ("Artificial Intelligence","Artificial Intelligence"),
        ("Machine Learning","Machine Learning"),
        ("Data Sceince","Data Science")
    ]
    Skills = models.CharField(default="",choices=skillChoice,max_length=40)
    Description = models.CharField(default="",max_length=150)
    mobile = models.IntegerField(default=0)


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
        ("Not Accepted","Not Accepted"),
        ("Accepted","Accepted"),
        ("Assigned","Assigned"),
        ("Delievred","Delievred"),
        ("Completed","Completed")
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
    Status = models.CharField(max_length=40,choices = status,default="Not Accepted")
    PaymentStatus = models.CharField(max_length=40,choices=payment,default="Not Paid")
    projectType = models.CharField(max_length=30,choices= type,default="")
    SentTO = models.ManyToManyField(Developer,blank=True)
    CompletePercentage = models.CharField(max_length=25,blank=True,choices=percentage,default=0)

    def __str__(self):
        return self.Title

class Bid(models.Model):
    userName = models.ForeignKey(Developer,on_delete=models.CASCADE)
    projectName = models.ForeignKey(Project,on_delete=models.CASCADE)
    bidAmount = models.IntegerField(default=0)

    class Meta:
        unique_together = [["userName","projectName"]]

    def __str__(self):
        return self.userName.user.username


class File(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    files = models.FileField(blank=True,upload_to="projects")
    fileName = models.CharField(max_length=100,blank=True)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.project.Title


class Payment(models.Model):
    projectName = models.ForeignKey(Project,null=True,on_delete=models.CASCADE)
    Amount = models.IntegerField(default=0)
    Date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.projectName.Title


class Assign(models.Model):
    userName = models.ForeignKey(Developer,on_delete=models.CASCADE)
    projectName = models.ForeignKey(Project,on_delete=models.CASCADE)
    Amount= models.IntegerField(default=0)
    Date = models.DateField(default=timezone.now)

    class Meta:
        unique_together = [["userName","projectName"]]


    def __str__(self):
        return self.projectName.Title
