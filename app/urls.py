from django.urls import path, re_path
from app import views
from django.conf import settings
from django.views.static import serve
from django.conf.urls import url

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path("tables",views.tables,name="tables"),
    path("maps",views.Maps,name="maps"),
    path("project/<str:id>/",views.project,name="project"),
    path("fileDownload",views.download,name="downlaod"),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
