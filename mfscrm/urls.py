from django.conf.urls import url, include
from django.contrib import admin
from crm.views import login_view, logout_view, register_view
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('', include('crm.urls')),

]
