from django.contrib import admin
from django.urls import path, include  # add this
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.views.static import serve

admin.site.site_header = "ExpertsMania Dashboard"
admin.site.site_title = "Admin panel"
admin.site.index_title = "Admin Panel"
urlpatterns = [
    url('jet/', include('jet.urls','jet')),
    path('jet/dashboard/', include('jet.dashboard.urls','jet-dashboard')), 
    path('admin/', admin.site.urls),          # Django admin route
    path("", include("authentication.urls")), # Auth routes - login / register
    path("", include("app.urls")),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
