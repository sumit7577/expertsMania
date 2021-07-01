from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models.query import prefetch_related_objects
from django.shortcuts import render, get_object_or_404, redirect
from django.template import context, loader
from django.http import HttpResponse, request
from django import template
from django.contrib.auth.models import User
from .models import Bid, Payment, Project, Developer, File,Client,Assign
import os
import zipfile
from datetime import datetime, timedelta
from django.conf import settings

projectId = None

@login_required(login_url="/login/")
def index(request):
    context = {}
    context['segment'] = 'index'
    if(not request.user.is_superuser and request.user.usertype.userType == "Developer"):
        try:
            request.user.developer
        except:
            return redirect("/profile")
        context["objects"] = Devfunc(request)
        print(context["objects"])
        context["api"] = graphApi(request)

    elif(not request.user.is_superuser and request.user.usertype.userType == "Client"):
        try:
            request.user.client
        except:
            return redirect("/profile")
        context["objects"] = ClientFunc(request)
        context["api"] = graphApi(request)

    elif(request.user.is_superuser):
        context["objects"] = AdminFunc(request)
        context["api"] = graphApi(request)

    else:
        return redirect("/register/")

    html_template = loader.get_template('index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        context['segment'] = load_template

        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:

        html_template = loader.get_template('page-500.html')
        return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def tables(request):
    table = {}
    table["segment"] = "tables"

    if(not request.user.is_superuser and request.user.usertype.userType == "Client"):
        data = Project.objects.filter(user=request.user.client)
        Projectdata = Assign.objects.filter(userName=request.user.developer.id)
        table["projectData"] = data
        table["objects"] = ClientFunc(request)

    elif(not request.user.is_superuser and request.user.usertype.userType == "Developer"):
        Projectdata = Assign.objects.filter(userName=request.user.developer.id)
        table["projectData"] = Projectdata
        table["objects"] = Devfunc(request)

    elif(request.user.is_superuser):
        AllProjects = Project.objects.all()
        table["projectData"] = AllProjects
        table["objects"] = AdminFunc(request)

    else:
        return redirect("/register/")

    return render(request, "tables.html", table)


@login_required(login_url="/login/")
def Maps(request):
    addProject = {}
    addProject["segment"] = "project"
    if request.user.is_superuser:
        addProject["objects"] = AdminFunc(request)

    elif(request.user.is_superuser and  request.user.usertype.userType == "Client"):
        addProject["objects"] = ClientFunc(request)

    elif(not request.user.is_superuser  and request.user.usertype.userType == "Developer"):
        data = Project.objects.filter(SentTO=request.user.developer.id)


        for i in data:
            Bid.objects.update_or_create(
                userName=request.user.developer, projectName=i)

        user = Bid.objects.filter(
            userName=request.user.developer.id, bidAmount=0)
        addProject["bidProject"] = user
        addProject["objects"] = Devfunc(request)

    if request.method == "POST":
        if(request.user.usertype.userType == "Client" or request.user.is_superuser):
            title = request.POST.get("title")
            projectType = request.POST.get("ptype")
            desc = request.POST.get("desc")
            user = Project(user=request.user.client, Title=title,
                           Description=desc, projectType=projectType)
            user.save()
            addProject["msg"] = "Project successfully Published"
            addProject["success"] = True

        elif(request.user.usertype.userType == "Developer"):
            Bidamount = request.POST.get("price")
            projectId = request.POST.get("none")
            try:
                Bid.objects.filter(projectName=projectId, userName=request.user.developer.id).update(
                    bidAmount=Bidamount)
                addProject["msg"] = "Bid Succesfully done"
                addProject["success"] = True
            except:
                addProject["msg"] = "Something went Wrong"

        else:
            return redirect("/register/")
    return render(request, "maps.html", addProject)


@login_required(login_url="/login/")
def project(request, id):
    data = {}
    data["id"] = id
    global projectId
    projectId = id
    projectData = Project.objects.filter(id=id)
    FilesData = File.objects.filter(project=id)
    data["ProjectData"] = projectData
    data["fileData"] = FilesData
    paid = 0
    projectMoney = Payment.objects.select_related("projectName").filter(projectName=id)

    for i in projectMoney:
        paid += i.Amount
    data["paid"] = paid
    create = projectData[0]
    if(not request.user.is_superuser and request.user.usertype.userType == "Developer"):
        projectPrice = Assign.objects.select_related("userName").filter(userName=request.user.developer.id,projectName=create)
        data["Price"] = projectPrice[0].Amount

    if request.method == "POST":
        if(not request.user.is_superuser and request.user.usertype.userType == "Client"):
            file = request.FILES["app"]
            File.objects.create(user=request.user,
                                project=create, files=file, fileName=file)
            data["message"] = "Project Updated Succcessfully"

        elif(not request.user.is_superuser and request.user.usertype.userType == "Developer"):
           
            file = request.FILES.getlist("app")
            for i in file:
                File.objects.create(user=request.user,
                                    project=create, files=i, fileName=i.name)
            status = request.POST.get("ptype")
            Project.objects.filter(id=id).update(CompletePercentage=status)
            data["message"] = "Project Updated Succcessfully"

        elif(request.user.is_superuser):
            success = adminPanel(request, id)
            data["message"] = success

        else:
            return redirect("/register/")
    if(request.user.is_superuser):
        sendTo = Project.objects.get(id=id)
        data["sended"] = sendTo.SentTO.all()
        BidData = Bid.objects.filter(projectName=id)
        data["SentTO"] = BidData
        names = Developer.objects.select_related("user").all()
        data["Names"] = names
        data["money"] = projectMoney
        assignedUser = Assign.objects.select_related("projectName").filter(projectName=id)
        data["assigned"] = assignedUser

    return render(request, "project.html", data)


@login_required(login_url="/login/")
def download(request):
    FileData = File.objects.filter(project=projectId)
    if len(FileData) == 0:
        return redirect("/tables")
    string = FileData[0].project.Title+".zip"
    app = settings.CORE_DIR+"\\"+string

    if os.path.exists(app):
        os.remove(app)

    with zipfile.ZipFile(string, "w", compression=zipfile.ZIP_DEFLATED) as file:
        for i in FileData:
            file.write(settings.MEDIA_ROOT+"\\projects\\"+i.fileName)
        file.close()

    with open(app, "rb") as f:
        response = HttpResponse(
            f.read(), content_type="application/files")
        response['Content-Disposition'] = 'inline;filename=' + \
            os.path.basename(app)
        try:
            return response
        except:
            return redirect("/tables")


def Devfunc(request):
    TotalData = []
    data = Assign.objects.select_related(
        "userName").filter(userName=request.user.developer.id)

    BidProjects = Bid.objects.select_related("userName").filter(
        userName=request.user.developer.id, bidAmount__gt=0)

    TodaysProjects = Bid.objects.filter(bidAmount=0).count()

    FileData = File.objects.select_related("user").filter(user=request.user.id)

    Earnings = 0
    for i in data:
        Earnings += i.Amount
    TotalData.append((data.count(), BidProjects.count(),
                     TodaysProjects, Earnings, BidProjects, FileData))

    return TotalData


def ClientFunc(request):
    TotalData = []
    projectData = Project.objects.select_related(
        "user").filter(user=request.user.client.id)
    ApprovedData = Project.objects.select_related("user").filter(
        user=request.user.client.id).exclude(Status="Not Accepted").count()
    TodaysProjects = Project.objects.filter(
        user=request.user.client.id, Date=datetime.today()).count()
    
    RejectedProject = Project.objects.select_related("user").filter(user=request.user.client.id,Status="Not Accepted")
    FileData = File.objects.select_related("user").filter(user=request.user.id)
    sales = 0
    for i in projectData:
        sales += i.ActualPrice
    TotalData.append((projectData.count(), ApprovedData,
                     TodaysProjects, sales, RejectedProject, FileData))

    return TotalData


def AdminFunc(request):
    TotalData = []
    projectData = Project.objects.all()
    TodaysProjects = Project.objects.filter(Date=datetime.today()).count()
    FileData = File.objects.select_related("user").filter(user=request.user.id)
    RejectedProject = Project.objects.filter(Status="Not Accepted")
    sales = 0
    TotalEarnings = 0
    for i in projectData:
        sales += i.CoderPrice
        TotalEarnings += i.ActualPrice
    TotalData.append((projectData.count(), TotalEarnings,
                     TodaysProjects, sales, RejectedProject, FileData))

    return TotalData


def graphApi(request):
    chartGraph = [0, 0, 0, 0, 0, 0, 0, 0]
    superuser = [0, 0, 0, 0, 0, 0, 0, 0]
    projectCounter = [0, 0, 0, 0, 0, 0, 0, 0]
    monthList = []
    tuple = (chartGraph, monthList, projectCounter,superuser)
    months = ["Unknown",
              "January",
              "Febuary",
              "March",
              "April",
              "May",
              "June",
              "July",
              "August",
              "September",
              "October",
              "November",
              "December"]
    month = datetime.today().month
    year = datetime.today().year
    TodayDate = datetime(year, month, 28)
    sample = datetime(year, month, 28)

    for i in range(0, 8):
        monthList.append(months[sample.month])
        sample -= timedelta(30)

    if (not request.user.is_superuser and request.user.usertype.userType == "Developer"):
        counter = 0
        chatData = Assign.objects.select_related(
            "userName").filter(userName=request.user.developer.id, Date__gte=TodayDate-timedelta(27)).filter(Date__lte=TodayDate)
        

        while counter <= 7:
            coderPrice = 0

            for i in chatData:
                coderPrice += i.Amount

            chartGraph[counter] = coderPrice
            projectCounter[counter] = chatData.count()
            TodayDate -= timedelta(30)
            chatData = Assign.objects.select_related(
                "userName").filter(userName=request.user.developer.id, Date__gte=TodayDate-timedelta(27)).filter(Date__lte=TodayDate)
            counter += 1

    elif(not request.user.is_superuser and request.user.usertype.userType == "Client"):

        counter = 0
        chatData = Project.objects.select_related(
            "user").filter(user=request.user.client.id, Date__gte=TodayDate-timedelta(27)).filter(Date__lte=TodayDate).exclude(Status="Not Accepted")

        while counter <= 7:
            actualPrice = 0

            for i in chatData:
                actualPrice += i.ActualPrice

            chartGraph[counter] = actualPrice
            projectCounter[counter] = chatData.count()
            TodayDate -= timedelta(30)
            chatData = Project.objects.select_related(
                "user").filter(user=request.user.client.id, Date__gte=TodayDate-timedelta(27)).filter(Date__lte=TodayDate).exclude(Status="Not Accepted")
            counter += 1

    elif(request.user.is_superuser):

        counter = 0
        chartData = Project.objects.filter(
            Date__gte=TodayDate-timedelta(27)).filter(Date__lte=TodayDate).exclude(Status="Not Accepted")
        

        while counter <= 7:
            coderPrice = 0
            Actualprice = 0

            for i in chartData:
                coderPrice += i.CoderPrice
                Actualprice += i.ActualPrice

            chartGraph[counter] = Actualprice
            superuser[counter] = coderPrice
            projectCounter[counter] = chartData.count()
            TodayDate -= timedelta(30)
            chartData = Project.objects.filter(Date__gte=TodayDate-timedelta(27)).filter(Date__lte=TodayDate).exclude(Status="Not Accepted")
            counter += 1

    else:
        return redirect("/register/")

    chartGraph.reverse()
    superuser.reverse()
    monthList.reverse()
    projectCounter.reverse()

    return tuple


def adminPanel(request, id):
    message = None

    if request.method == "POST":
        projectName = request.POST.get("name")
        projectType = request.POST.get("ptype")
        clientPrice = request.POST.get("price")
        coderPrice = request.POST.get("cprice")
        sendToBid = request.POST.getlist("sender")
        data = Project.objects.get(id=id)
        data.SentTO.set(sendToBid)
        message = "Project Successfully Updated"
        file = request.FILES.getlist("app")
        for i in file:
            File.objects.create(user=request.user,
                                project=data, files=i, fileName=i.name)

        message = "Project Successfully Updated"
        assignTo = request.POST.get("assign")
        projectStatus = request.POST.get("prstatus")
        paymentStatus = request.POST.get("pstatus")
        clientPaid = request.POST.get("clientPaid")
        description = request.POST.get("desc")
        assignAmount = request.POST.get("amount")

        Project.objects.filter(id=id).update(Title=projectName, projectType=projectType, ActualPrice=clientPrice,
                                             CoderPrice=coderPrice, Status=projectStatus, PaymentStatus=paymentStatus, Description=description)
        message = "Project Successfully Updated"

        if clientPaid != "":
            Payment.objects.create(projectName=data, Amount=clientPaid)
            message = "Project Successfully Updated"
        if assignAmount != "":
            try:
                data = Developer.objects.filter(id=assignTo)
                projectData = Project.objects.filter(id=id)
                Assign.objects.create(userName=data[0],Amount=assignAmount,projectName=projectData[0])
            except:
                message ="User is Already Assigned"
           

    return message
