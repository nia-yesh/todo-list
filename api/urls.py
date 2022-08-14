from django.contrib import admin
from django.urls import path, include

from api.settings import API_BASE_URL

urlpatterns = [
    path('admin/', admin.site.urls),
    path(API_BASE_URL + 'account/', include('apps.accounts.urls')),
    path(API_BASE_URL + 'project/', include('apps.projects.urls')),
]
