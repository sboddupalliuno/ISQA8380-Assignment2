from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('portfolio.urls')),
    path('', include('django.contrib.auth.urls')),
]
