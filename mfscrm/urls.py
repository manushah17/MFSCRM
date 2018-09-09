from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('crm.urls')),
    url(r'^accounts/login/$', views.login, name='login'),
    url(r'^accounts/logout/$', views.logout, name='logout', kwargs={'next_page': '/'}),
]
