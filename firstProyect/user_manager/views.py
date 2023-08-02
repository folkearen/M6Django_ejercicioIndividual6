from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import *
# from .forms import LoginForm
from .forms import forms
from .models import Usuario
from django.contrib.auth.models import  Group
import time


# Create your views here.



def signUp(request):
    if request.method == "POST":
            formulario_post = forms.SignUp(request.POST)
            if formulario_post.is_valid():
                # Guardar el usuario con commit=False para que la contraseña se encripte correctamente
                user = formulario_post.save(commit=False)
                # Asegurarse de que la contraseña se encripte utilizando el método save() personalizado
                grupo_seleccionado = formulario_post.cleaned_data['tipo_usuario']
                if grupo_seleccionado == 'admin':
                    grupo = Group.objects.get(name='admin')
                elif grupo_seleccionado == 'usuario_comun':
                    grupo = Group.objects.get(name='usuario_comun')
                elif grupo_seleccionado == 'permission_manger':
                    grupo = Group.objects.get(name='permission_manger')
                else:
                # Caso predeterminado: en caso de un valor inesperado
                    grupo = None
                user.save()
                if grupo:
                    user.groups.add(grupo)
                login(request, user) 
                #login(request, user)
                return redirect('user_manager:successfulRegistration')

            else:
                # Capturar la excepción de ValidationError y agregar el mensaje de error al formulario
                error_message = None
                if '__all__' in formulario_post.errors:
                    error_message = formulario_post.errors['__all__'][0]
                    return render(request, 'user_manager/signUp.html', {
                        'form': formulario_post,
                        'error': error_message
                    })

    return render(request,'user_manager/signUp.html',{
         'form': forms.SignUp()
        })

    # if request.method == "POST" and request.POST['password'] != request.POST['confirm_password']: 
    #     return render(request,'user_manager/signUp.html',{
    #     'form': forms.signUp(),
    #     'error': 'Las contraseñas no coinciden'
    #     })   

def successfulRegistration(request):
    numero_usuario = Usuario.objects.count()
    return render(request,'user_manager/successfulRegistration.html', {
            'numero_usuario' : numero_usuario 
        } )


class MyLoginView(LoginView):
    form_class =  forms.LoginForm
    template_name = 'user_manager/login.html'  # Reemplaza esto con el nombre de tu template de inicio de sesión
    error_messages = {
    'invalid_login': "El correo electrónico o la contraseña no son válidos. Por favor, inténtalo de nuevo.",
    'inactive': "Esta cuenta está inactiva.",
    'unregistered_email': "El correo electrónico ingresado no está registrado. Por favor, regístrese primero.",
    }

    def get_invalid_login_error(self):
        # Verificar si el error es de correo no registrado y agregar el mensaje de error personalizado
        if 'invalid_login' in self.request.GET:
            if 'unregistered_email' in self.request.GET['invalid_login']:
                return self.error_messages['unregistered_email']
            else:
                return self.error_messages['invalid_login']
        return super().get_invalid_login_error()

@login_required
def userAccount(request):
    return render(request, 'user_manager/userAccount.html')

# def mostrarUsuarios(request):
#     usuarios =  Usuario.objects.count()
#     return render(request, 'user_manager/showUsers.html', {
#         "usuarios":usuarios
#     })

    # <script>
    #     setTimeout(function() {
    #         window.location.href = '/segunda_pagina/';
    #     }, 5000);  // Redirigir después de 5 segundos (5000 milisegundos)
    # </script>