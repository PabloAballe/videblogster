from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.core.validators import RegexValidator

class Porfile(models.Model):
    id_porfile=models.AutoField(primary_key=True, auto_created = True)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, help_text="Nombre de usuario")
    imagen_perfil=models.ImageField(upload_to='porfile/images', default="default/porfile.png", help_text="Imágen de Perfil")
    cover=models.ImageField(upload_to='porfile/images/cover', default="default/cover.png",help_text="Sube tu cover")
    bio=models.CharField(max_length=300,help_text="Escriba aqui su biografia", null=True, blank=True)
    vistas=models.IntegerField(default=0)
    website=models.CharField(max_length=100,help_text="Ingresa tu sitio web", default="", null=True, blank=True)
    paypal=models.EmailField(max_length=254, default="", help_text="Tu cuenta de PayPal para recibir los pagos")
    total_post=models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Porfiles"

    def __str__(self):
        return f"Usuario: {self.usuario}"

def create_user_profile(sender, instance, created, **kwargs):
    if created:
       profile, created = Porfile.objects.get_or_create(usuario=instance)

post_save.connect(create_user_profile, sender=User)



class Categorias(models.Model):
    id_categoria=models.AutoField(primary_key=True, auto_created = True)
    usuario=models.ForeignKey(User, on_delete=models.CASCADE)
    categoria_nombre=models.CharField(max_length=100,help_text="Título de la categoria")
    categoria_api=models.CharField(max_length=50,help_text="Término de búsqueda en la api",default="")
    creada_el = models.DateTimeField(default=timezone.now)


    class Meta:
        verbose_name_plural = "Categorias"

    def __str__(self):
        return f"{self.categoria_nombre}"


class ExtensionValidator(RegexValidator):
    def __init__(self, extensions, message=None):
        if not hasattr(extensions, '__iter__'):
            extensions = [extensions]
        regex = '\.(%s)$' % '|'.join(extensions)
        if message is None:
            message = 'File type not supported. Accepted types are: %s.' % ', '.join(extensions)
        super(ExtensionValidator, self).__init__(regex, message)

    def __call__(self, value):
        super(ExtensionValidator, self).__call__(value.name)



# def validate_file_extensions(value):
#   import os
#   ext = os.path.splitext(value.name)[1]
#   valid_extensions = ['.mkv','.mp4','.mov', '.wmv', '.wma']
#   if not ext in valid_extensions:
#     raise ValidationError(u'File not supported!')

class Post(models.Model):
    id_post=models.AutoField(primary_key=True, auto_created = True)
    titulo=models.CharField(max_length=100,help_text="Título del video")
    descripcion=models.TextField(help_text="Descripción corta del video", default="", null=True, blank=True)
    imagen_principal=models.ImageField(upload_to='posts/images',help_text="Cover de tu video")
    video=models.FileField(upload_to='videos/',help_text="Sube tu video")
    imagen_url=models.CharField(max_length=300,help_text="URL de la imagen", default="", null=True, blank=True)
    video_url=models.CharField(max_length=300,help_text="URL de la imagen", default="", null=True, blank=True, )
    autor=models.ForeignKey(Porfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    publicado=models.BooleanField(default=False)
    monetizar=models.BooleanField(default=False,help_text="¿Queires monetizar tu video?")
    categoria=models.ForeignKey(Categorias, on_delete=models.CASCADE,help_text="Elige la categoria de tu video")
    visitas=models.IntegerField(default=0)




    class Meta:
        verbose_name_plural = "Videos"

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse('post_details', args=[str(self.id_post)])



class Comentario(models.Model):
    id_post=models.AutoField(primary_key=True, auto_created = True)
    author_comentario=models.ForeignKey(Porfile, on_delete=models.CASCADE)
    post_comentario=models.ForeignKey(Post, on_delete=models.CASCADE)
    comentario= models.TextField(help_text="Escriba aquí su comentario")
    publicado=models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)


    class Meta:
        verbose_name_plural = "Comentarios"

    def __str__(self):
        return f"Comentario con fecha: {self.created_at}"


class PostGuardado(models.Model):
    id_post_guardado=models.AutoField(primary_key=True, auto_created = True)
    usuario=models.ForeignKey(User, on_delete=models.CASCADE)
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    guardado_el = models.DateTimeField(default=timezone.now)


    class Meta:
        verbose_name_plural = "Videos Guardados"

    def __str__(self):
        return f"Guardado el video con fecha: {self.guardado_el}"

class Seguidores(models.Model):
    id_seguidor=models.AutoField(primary_key=True, auto_created = True)
    sigue=models.ForeignKey(User, on_delete=models.DO_NOTHING,related_name="Sigue")
    seguido=models.ForeignKey(User, on_delete=models.DO_NOTHING,related_name="Seguido")
    seguiendo_desde = models.DateTimeField(default=timezone.now)


    class Meta:
        verbose_name_plural = "Seguidores"

    def __str__(self):
        return f"Seguidos desde: {self.seguiendo_desde}"

class Condicion(models.Model):
    id_Condicion=models.AutoField(primary_key=True, auto_created = True)
    articulo=models.TextField(help_text="Escriba aquí sus condiciones")
    created_at = models.DateTimeField(default=timezone.now)


    class Meta:
        verbose_name_plural = "Condiciones"

    def __str__(self):
        return f"Condicion creada el : {self.created_at}"

class PostLike(models.Model):
    id_post_like=models.AutoField(primary_key=True, auto_created = True)
    usuario=models.ForeignKey(User, on_delete=models.CASCADE)
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    like_post_el = models.DateTimeField(default=timezone.now)


    class Meta:
        verbose_name_plural = "Videos Likes"

    def __str__(self):
        return f"Like el video con fecha: {self.guardado_el}"


