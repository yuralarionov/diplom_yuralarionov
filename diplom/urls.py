"""
URL configuration for diplom project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib.auth import views as auth_views

from webapp.views import index, about, contact, services, account, register, logout_view, panel_admin, add_order_index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('services/', services, name='services'),
    path('account/', account, name='account'),
    path('panel_admin/', panel_admin, name='panel_admin'),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name='login'),
    path('register/', register, name='register'),
    path('logout/', logout_view, name='logout'),
    path('add_order_index/', add_order_index, name='add_order_index')
]
