from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import context, loader
from django.http import HttpResponse, request
from django import template
from django.contrib.auth.models import User
from .models import Bid, Payment, Project, Developer, File, Client, Assign
import os
import zipfile
from datetime import datetime, timedelta
from django.conf import settings

projectId = None


@login_required(login_url="/login/")
def index(request):
    global projectId
    projectId = None
    context = {}
    context['segment'] = 'index'
    if(not request.user.is_superuser and request.user.usertype.userType == "Developer"):
        try:
            request.user.developer
        except:
            return redirect("/register/")
        context["objects"] = Devfunc(request)
        context["api"] = graphApi(request)

    elif(not request.user.is_superuser and request.user.usertype.userType == "Client"):
        try:
            request.user.client
        except:
            return redirect("/register/")
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
        filterData = []
        data = Project.objects.filter(user=request.user.client)
        table["projectData"] = data
        table["objects"] = ClientFunc(request)
        filter = request.GET.get("filter")

        if filter:
            for i in range(0, len(data)):
                if((filter in str(data[i].id)) or (filter in data[i].Title.lower()) or (filter in data[i].Status.lower()) or (filter in str(data[i].ActualPrice)) or (filter in data[i].projectType.lower()) or (filter in data[i].PaymentStatus.lower()) ):
                    filterData.append(data[i])
            if(len(filterData) > 0):
                table["projectData"] = filterData

    elif(not request.user.is_superuser and request.user.usertype.userType == "Developer"):
        filterData = []
        Projectdata = Assign.objects.filter(
            userName=request.user.developer)
        table["projectData"] = Projectdata
        table["objects"] = Devfunc(request)
        filter = request.GET.get("filter")

        if filter:
            for i in range(0, len(Projectdata)):
                if((filter in str(Projectdata[i].projectName.id)) or (filter in Projectdata[i].projectName.Title.lower()) or (filter in Projectdata[i].projectName.Status.lower()) or (filter in Projectdata[i].projectName.user.user.username.lower()) or (filter in str(Projectdata[i].Amount)) or (filter in Projectdata[i].projectName.projectType.lower()) ):
                    filterData.append(Projectdata[i])
            if(len(filterData) > 0):
                table["projectData"] = filterData

    elif(request.user.is_superuser):
        filterData = []
        AllProjects = Project.objects.all()
        table["projectData"] = AllProjects
        table["objects"] = AdminFunc(request)
        filter = request.GET.get("filter")

        if filter:
            for i in range(0, len(AllProjects)):
                if((filter in str(AllProjects[i].id)) or (filter in AllProjects[i].Title.lower()) or (filter in AllProjects[i].Status.lower()) or (filter in AllProjects[i].user.user.username.lower()) or (filter in str(AllProjects[i].ActualPrice)) or (filter in str(AllProjects[i].CoderPrice)) or (filter in AllProjects[i].projectType.lower()) or (filter in AllProjects[i].PaymentStatus.lower()) ):
                    filterData.append(AllProjects[i])
            if(len(filterData) > 0):
                table["projectData"] = filterData

    else:
        return redirect("/register/")

    return render(request, "tables.html", table)


@login_required(login_url="/login/")
def Maps(request):
    addProject = {}
    addProject["segment"] = "project"
    client = Client.objects.all()
    addProject["Client"] = client
    if request.user.is_superuser:
        addProject["objects"] = AdminFunc(request)

    elif(not request.user.is_superuser and request.user.usertype.userType == "Client"):
        addProject["objects"] = ClientFunc(request)

    elif(not request.user.is_superuser and request.user.usertype.userType == "Developer"):
        data = Project.objects.filter(SentTO=request.user.developer.id)

        for i in data:
            Bid.objects.update_or_create(
                userName=request.user.developer, projectName=i)

        user = Bid.objects.filter(
            userName=request.user.developer.id, bidAmount=0)
        addProject["bidProject"] = user
        addProject["objects"] = Devfunc(request)

    if request.method == "POST":
        if(not request.user.is_superuser and request.user.usertype.userType == "Client"):
            title = request.POST.get("title")
            projectType = request.POST.get("ptype")
            desc = request.POST.get("desc")
            file = request.FILES.getlist("app")
            deadline = request.POST.get("deadline")
            user = Project(user=request.user.client, Title=title,
                           Description=desc, projectType=projectType,ClientDeadline=deadline)
            user.save()
            
            for i in file:
                File.objects.create(user=request.user,
                                    project=user, files=i, fileName=i.name)
            
            addProject["msg"] = "Project successfully Published"
            addProject["success"] = True

        elif(request.user.is_superuser):
            title = request.POST.get("title")
            projectType = request.POST.get("ptype")
            desc = request.POST.get("desc")
            clientname = request.POST.get("client")
            file = request.FILES.getlist("app")
            deadline = request.POST.get("deadline")
            clientData = Client.objects.filter(id=clientname)
            user = Project(user=clientData[0], Title=title,
                           Description=desc, projectType=projectType,ClientDeadline= deadline)
            user.save()
            for i in file:
                File.objects.create(user=request.user,
                                    project=user, files=i, fileName=i.name)

            addProject["msg"] = "Project successfully Published"
            addProject["success"] = True

        else:
            return redirect("/register/")
    return render(request, "maps.html", addProject)


@login_required(login_url="/login")
def developerBid(request,id):
    if(not request.user.usertype.userType == "Developer"):
        return redirect("/")
    message = None
    projectData = {}
    BidProjects = Bid.objects.filter(id=id)
    global projectId
    projectId = BidProjects[0].projectName.id

    projectData["bidData"] = BidProjects
    if request.method == "POST":
        BidAmount = request.POST.get("price")
        try:
            Bid.objects.filter(id=id).update(bidAmount=BidAmount)
            projectData["message"] = "Project Successfully Bided"
            return redirect("/maps")
        except:
            projectData["message"] = "Something error happened"
    
    return render(request,"bid.html",projectData)


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
    projectMoney = Payment.objects.select_related(
        "projectName").filter(projectName=id)

    for i in projectMoney:
        paid += i.Amount
    data["paid"] = paid
    create = projectData[0]


    if(not request.user.is_superuser and request.user.usertype.userType == "Developer"):
        projectPrice = Assign.objects.select_related("userName").filter(
            userName=request.user.developer, projectName=create)
        data["Price"] = projectPrice[0].Amount
        data["deadline"] = projectPrice[0].DeveloperDeadline

    if request.method == "POST":
        if(not request.user.is_superuser and request.user.usertype.userType == "Client"):
            file = request.FILES.getlist("app")
            discussion = request.POST.get("client")
            for i in file:
                File.objects.create(user=request.user,
                                    project=create, files=i, fileName=i.name)
            Project.objects.filter(id=id).update(ClientDiscussion=discussion)
            data["message"] = "Project Updated Succcessfully"

        elif(not request.user.is_superuser and request.user.usertype.userType == "Developer"):

            file = request.FILES.getlist("app")
            for i in file:
                File.objects.create(user=request.user,
                                    project=create, files=i, fileName=i.name)
            status = request.POST.get("ptype")
            discussion = request.POST.get("developer")
            Project.objects.filter(id=id).update(CompletePercentage=status,DeveloperDiscussion=discussion)
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
        assignedUser = Assign.objects.select_related(
            "projectName").filter(projectName=id)
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
            return redirect("/")


def Devfunc(request):
    TotalData = []
    data = Assign.objects.select_related(
        "userName").filter(userName=request.user.developer.id)

    data2 = Assign.objects.select_related("userName").filter(
        userName=request.user.developer.id, projectName__Status="Completed")

    BidProjects = Bid.objects.select_related("userName").filter(
        userName=request.user.developer.id, bidAmount__gt=0)
    counter = BidProjects.count()

    for i in range(0, len(data)):
        BidProjects = Bid.objects.select_related("userName").filter(
            userName=request.user.developer.id, bidAmount__gt=0).exclude(projectName=data[i].projectName)

    if(len(BidProjects) == 2):
        BidProjects = BidProjects[1:]

    elif(len(BidProjects) == 1):
        BidProjects = []
    else:
        BidProjects = BidProjects

    TodaysProjects = Bid.objects.filter(bidAmount=0).count()

    AssignData = Assign.objects.select_related("userName").filter(
        userName=request.user.developer.id).exclude(projectName__Status="Completed")

    Earnings = 0
    for i in data2:
        Earnings += i.Amount
    TotalData.append((data.count(), counter,
                     TodaysProjects, Earnings, BidProjects, AssignData,data2.count()))

    return TotalData


def ClientFunc(request):
    TotalData = []
    projectData = Project.objects.select_related(
        "user").filter(user=request.user.client.id).count()

    projectData2 = Project.objects.select_related("user").filter(
        user=request.user.client.id, Status="Completed")

    ApprovedData = Project.objects.select_related("user").filter(
        user=request.user.client.id).exclude(Status="Rejected").exclude(Status="Pending").count()

    TodaysProjects = Project.objects.filter(
        user=request.user.client.id, Status="Pending").count()

    RejectedProject = Project.objects.select_related("user").filter(
        user=request.user.client.id, Status="Rejected")

    ApproveData = Project.objects.select_related("user").filter(
        user=request.user.client.id, Status="Accepted")
    sales = 0

    for i in projectData2:
        sales += i.ActualPrice

    TotalData.append((projectData, ApprovedData,
                     TodaysProjects, sales, RejectedProject, ApproveData,projectData2.count()))

    return TotalData


def AdminFunc(request):
    TotalData = []
    projectData = Project.objects.all()

    projectData2 = Project.objects.filter(Status="Completed")
    TodaysProjects = Project.objects.filter(Date=datetime.today())

    RejectedProject = Project.objects.filter(Status="Rejected")
    sales = 0
    TotalEarnings = 0
    

    for i in projectData2:
        sales += i.CoderPrice
        TotalEarnings += i.ActualPrice
    revenue = TotalEarnings-sales
    TotalData.append((projectData.count(), TotalEarnings,
                     TodaysProjects.count(), sales, RejectedProject, TodaysProjects,projectData2.count(),RejectedProject.count(),revenue))

    return TotalData


def graphApi(request):
    chartGraph = [0, 0, 0, 0, 0, 0, 0, 0]
    superuser = [0, 0, 0, 0, 0, 0, 0, 0]
    projectCounter = [0, 0, 0, 0, 0, 0, 0, 0]
    monthList = []
    tuple = (chartGraph, monthList, projectCounter, superuser)
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
            "userName").filter(userName=request.user.developer.id, Date__gte=TodayDate-timedelta(27), projectName__Status="Completed").filter(Date__lte=TodayDate)

        while counter <= 7:
            coderPrice = 0

            for i in chatData:
                coderPrice += i.Amount

            chartGraph[counter] = coderPrice
            projectCounter[counter] = chatData.count()
            TodayDate -= timedelta(30)
            chatData = Assign.objects.select_related(
                "userName").filter(userName=request.user.developer.id, Date__gte=TodayDate-timedelta(27), projectName__Status="Completed").filter(Date__lte=TodayDate)
            counter += 1

    elif(not request.user.is_superuser and request.user.usertype.userType == "Client"):

        counter = 0
        chatData = Project.objects.select_related(
            "user").filter(user=request.user.client.id, Date__gte=TodayDate-timedelta(27), Status="Completed").filter(Date__lte=TodayDate)

        while counter <= 7:
            actualPrice = 0

            for i in chatData:
                actualPrice += i.ActualPrice

            chartGraph[counter] = actualPrice
            projectCounter[counter] = chatData.count()
            TodayDate -= timedelta(30)
            chatData = Project.objects.select_related(
                "user").filter(user=request.user.client.id, Date__gte=TodayDate-timedelta(27), Status="Completed").filter(Date__lte=TodayDate)
            counter += 1

    elif(request.user.is_superuser):

        counter = 0
        chartData = Project.objects.filter(
            Date__gte=TodayDate-timedelta(27), Status="Completed").filter(Date__lte=TodayDate)

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
            chartData = Project.objects.filter(
                Date__gte=TodayDate-timedelta(27), Status="Completed").filter(Date__lte=TodayDate)
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
        percentage = request.POST.get("percent")
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
        developerDeadline= request.POST.get("deadline")
        clientDeadline = request.POST.get("clientdeadline")
        currencyCode = request.POST.get("clientCurrency")

        Project.objects.filter(id=id).update(Title=projectName, projectType=projectType, ActualPrice=clientPrice,
                                             CoderPrice=coderPrice, Status=projectStatus, PaymentStatus=paymentStatus, Description=description,currencyCode=currencyCode,CompletePercentage=percentage)
        message = "Project Successfully Updated"

        if clientPaid != "":
            Payment.objects.create(projectName=data, Amount=clientPaid)
            message = "Project Successfully Updated"
        if assignAmount != "":
            try:
                data = Developer.objects.filter(id=assignTo)
                projectData = Project.objects.filter(id=id)
                Assign.objects.create(
                    userName=data[0], Amount=assignAmount, projectName=projectData[0],DeveloperDeadline= developerDeadline)
            except:
                message = "User is Already Assigned"
        if clientDeadline != "":
            Project.objects.filter(id=id).update(Title=projectName, projectType=projectType, ActualPrice=clientPrice,
                                             CoderPrice=coderPrice, Status=projectStatus, PaymentStatus=paymentStatus, Description=description,ClientDeadline = clientDeadline,currencyCode=currencyCode)
            message = "Project Successfully Updated"


    return message
