from django.contrib import admin
from .models import Client,Project,userType,Developer,Bid,File,Payment,Assign

# Register your models here.
admin.site.register(Client)
admin.site.register(Developer)
admin.site.register(userType)
admin.site.register(Bid)
admin.site.register(File)
admin.site.register(Project)
admin.site.register(Payment)
admin.site.register(Assign)