from django import forms
from .models import Comentario
from .models import Post
from .models import Porfile
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django.contrib.auth.models import User

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
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email')

class PorfileForm(forms.ModelForm):
    class Meta:
        model = Porfile
        fields = ('imagen_perfil', 'bio', 'website', 'cover', 'paypal')
