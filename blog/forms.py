from django import forms
from .models import Comentario
from .models import Post
from .models import Porfile
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import CharField, Form, PasswordInput


# Extendemos del original
class UCFWithEmail(UserCreationForm):
    # Ahora el campo username es de tipo email y cambiamos su texto
    #username = forms.EmailField(label="Correo electrónico")
    username = forms.CharField(label = "Escriba su nombre de usuario aquí.", help_text="Escriba su nombre de usuario aquí.")
    password1 = forms.CharField(widget=PasswordInput(), help_text="Escriba su contraseña aquí.")
    password2 = forms.CharField(widget=PasswordInput(), help_text="Confirme su contraseña.")
    email = forms.EmailField(help_text = "Escriba su email aquí.")
    class Meta:
        model = User
        fields = ["username","email", "password1", "password2"]
        labels = {
            'username': ('Nombre de usuario'),
            'email': ("Su email"),
            'password1': ("Contraseña"),
            'password2': ("Confirme su contraseña"),
        }
        help_texts = {
            'name': ('Escriba su nombre de usuario aquí.'),
            'email': ('Escriba su email aquí.'),
            'password1': ('Escriba su contraseña aquí.'),
            'password2': ('Confirme su contraseña.'),
        }
    
        


# Extendemos del original
class AFWithEmail(AuthenticationForm):
    # Ahora el campo username es de tipo email y cambiamos su texto
    #username = forms.EmailField(label="Correo electrónico")
    username = forms.CharField(label = "Escriba su nombre de usuario aquí.", help_text="Escriba su nombre de usuario aquí.")
    password = forms.CharField(widget=PasswordInput(), help_text="Escriba su contraseña aquí.")
    
    class Meta:
        model = User
        fields = ["username", "password"]

class SheachForm(forms.Form):
    shearch = forms.CharField( label="", max_length=100 , widget= forms.TextInput
                           (attrs={'class':'form-control mr-sm-2'}))

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ('comentario',)
        comentario = forms.CharField( label="", max_length=100 , widget= forms.TextInput
                               (attrs={'class':'input'}))
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('titulo', 'descripcion', 'imagen_principal', 'categoria','articulo')
        widgets = {
            'articulo': SummernoteWidget(),
        }


class UserForm(forms.ModelForm):
    username = forms.CharField(label = "Escriba su nombre de usuario aquí.", help_text="Escriba su nombre de usuario aquí.")
    first_name = forms.CharField(label = "Escriba su nombre aquí.", help_text="Escriba su nombre aquí.")
    last_name = forms.CharField(label = "Escriba su apellido aquí.", help_text="Escriba su apellido aquí.")
    email = forms.CharField(label = "Escriba su email aquí.", help_text="Escriba su email aquí.")
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email')

class PorfileForm(forms.ModelForm):
    class Meta:
        model = Porfile
        fields = ('imagen_perfil', 'bio', 'website', 'cover', 'paypal')
