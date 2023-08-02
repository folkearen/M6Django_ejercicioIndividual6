from django.shortcuts import render
from user_manager.models import Usuario
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def homePage(request):
    cantidad_usuarios = Usuario.objects.count()
    return render(request,'home/index.html', {
        'cantidad_usuarios' : cantidad_usuarios
    })

def homeContacto(request):
    return render(request, 'home/contacto.html', {})

