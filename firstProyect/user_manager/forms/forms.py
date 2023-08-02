from django import forms
from django.contrib.auth.forms import AuthenticationForm
from ..models import *
import re
#Etiqueta meta
#model: Este atributo se usa cuando se desea crear un formulario basado en un modelo (ModelForm). Indica el modelo en el que se basará el formulario, y Django generará automáticamente los campos del formulario según los campos del modelo.
# fields: Se utiliza en los ModelForms para indicar qué campos del modelo se incluirán en el formulario. Puedes especificar una lista de nombres de campos que deseas mostrar en el formulario.
# exclude: Otra opción para ModelForms, donde se puede especificar una lista de campos que no se incluirán en el formulario.
# widgets: Te permite definir widgets personalizados para los campos del formulario. Los widgets controlan cómo se renderizan los campos en el frontend.
# labels: Puedes proporcionar etiquetas personalizadas para los campos del formulario mediante un diccionario donde las claves son los nombres de los campos y los valores son las etiquetas deseadas.
# help_texts: Similar a labels, te permite proporcionar texto de ayuda personalizado para los campos mediante un diccionario.
# error_messages: Permite personalizar los mensajes de error para campos específicos en caso de que la validación falle.

class SignUp(forms.ModelForm):
    nombre = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'singup_input', 'placeholder': 'Albus Percival Wulfric Brian '}))
    apellido = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'singup_input', 'placeholder': ' Dumbledore'}))
    email = forms.CharField(max_length=254, required=True, widget=forms.TextInput(attrs={'class': 'singup_input', 'placeholder': 'albusD@lalechuza.com'}))
    password = forms.CharField(max_length=12, required=True,  widget=forms.PasswordInput(attrs={'class': 'singup_input', 'placeholder': '****'}))
    confirm_password = forms.CharField(max_length=12, required=True, widget=forms.PasswordInput(attrs={'class': 'singup_input', 'placeholder': '****'}))
    
    campos = (
        ('admin', 'Administrador'),
        ('usuario_comun', 'Usuario comun'),
        ('permission_manger', 'Moderador de permisos')
    )
    tipo_usuario = forms.ChoiceField(choices=campos)
    
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        email = cleaned_data.get('email')

        if email and Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado. Por favor, utiliza otro.")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden. Vuelve a escribirlas.")

        prohibited_patterns = r'\s'
        if  re.search(prohibited_patterns, password):
            raise forms.ValidationError("La contraseña no puede tener espacios")
        
        allowed_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)'
        if not re.search(allowed_pattern, password):
            raise forms.ValidationError("La contaseña debe poseer al menos una minúscula, una mayúscula y un número.")
        

        if len(password) < 8:
            raise forms.ValidationError("La contaseña debe poseer al menos 8 caracteres")


    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data['password']
        user.set_password(password)
        if commit:
            user.save()
        return user
  

class LoginForm(AuthenticationForm):
    username =forms.EmailField(max_length=254, widget=forms.TextInput(attrs={'class': 'login_input', 'placeholder': 'Ej: tunombre@example.com'}))
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'class': 'login_input', 'placeholder': '***********'}))
    
    error_messages = {
        'invalid_login': "El correo electrónico o la contraseña no son válidos. Por favor, inténtalo de nuevo.",
        'inactive': "Esta cuenta está inactiva.",
    }


# def clean(self):: Este es el método clean() de un formulario personalizado en Django. Es un método especial que se utiliza para realizar validaciones personalizadas antes de que los datos del formulario se guarden en la base de datos.

# cleaned_data = super().clean(): Aquí, llamamos al método clean() de la clase base (super()) para obtener el diccionario cleaned_data, que contiene los datos del formulario limpios y validados.

# password = cleaned_data.get('password'): Obtenemos el valor del campo de contraseña (password) del diccionario cleaned_data. cleaned_data.get() es utilizado para obtener los valores de los campos limpios después de haber pasado por todas las validaciones.

# confirm_password = cleaned_data.get('confirm_password'): Obtenemos el valor del campo de confirmación de contraseña (confirm_password) del diccionario cleaned_data.

# if password and confirm_password and password != confirm_password:: Aquí verificamos si tanto la contraseña como la confirmación de contraseña existen y si son diferentes. Si esto ocurre, significa que las contraseñas no coinciden y lanzamos una excepción forms.ValidationError con un mensaje de error indicando que las contraseñas no coinciden.


# def save(self, commit=True):: Este es el método save() personalizado del formulario. Sobrescribimos este método para personalizar cómo se guarda el objeto del modelo en la base de datos.

# user = super().save(commit=False): Llamamos al método save() de la clase base (super()) con commit=False, lo que crea una instancia del modelo Usuario pero no la guarda en la base de datos todavía.

# password = self.cleaned_data['password']: Obtenemos la contraseña ingresada por el usuario desde el diccionario cleaned_data utilizando el campo password.

# user.set_password(password): Utilizamos el método set_password() del modelo de usuario (Usuario) para encriptar la contraseña antes de guardarla en la base de datos. Esto asegura que la contraseña se almacene de forma segura y encriptada.

# if commit: user.save(): Si commit es True, guardamos el usuario en la base de datos utilizando el método save() del modelo de usuario. Si commit es False, el usuario no se guarda inmediatamente, lo que nos permite realizar más modificaciones en el objeto antes de guardarlo.

# return user: Finalmente, devolvemos el objeto del usuario, que ahora tiene la contraseña encriptada, para que pueda ser utilizado o procesado posteriormente.

# Con este código, cuando utilizas el método save() en el formulario, la contraseña ingresada se encriptará automáticamente antes de guardarla en la base de datos.