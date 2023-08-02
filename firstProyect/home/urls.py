from django.contrib import admin
from django.urls import path
from .views import *

app_name  = 'home'
urlpatterns = [
    path('', homePage, name="home"),
    path('contacto/', homeContacto, name="contacto")

]