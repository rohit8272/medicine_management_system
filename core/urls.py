"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from medicine_system.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('add_medicine/' , add_medicine),
    path('get_medicine/' ,get_medicine),
    path('get_medicine_by_id/<uuid>/' ,get_medicine_by_id),
    path('update_medicine/<uuid>/' , update_medicine),
    path('delete_medicine/<uuid>/' ,delete_medicine),
    path('add_customer/' , add_customer),
    path('get_customer/' , get_customer),
    path('get_customer_by_id/<uuid>/' , get_customer_by_id),
    path('update_customer/<uuid>/' , update_customer),
    path('delete_customer/<uuid>/', delete_customer)


]
