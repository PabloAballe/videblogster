from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify


class Porfile(models.Model):
    id_porfile=models.AutoField(primary_key=True, auto_created = True)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    imagen_perfil=models.ImageField(upload_to='porfile/images', default="default/porfile.png", help_text="Imágen de Perfil")
    cover=models.ImageField(upload_to='porfile/images/cover', default="default/cover.png",help_text="Sube tu cover")
    bio=models.CharField(max_length=300,help_text="Escriba aqui su biografia", null=True, blank=True)
    vistas=models.IntegerField(default=0)
    website=models.CharField(max_length=100,help_text="Ingresa tu sitio web", default="", null=True, blank=True)
    email=models.EmailField(max_length=300,help_text="Tu Email", default="", null=True, blank=True)
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

CHOICES = (
    ('hogar','HOGAR'),
    ('deportes', 'DEPORTES'),
    ('tecnologia','TECNOLOGIA'),
    ('ciencia','CIENCIA'),
    ('salud','SALUD'),
    ('estilodevida','ESTILO-DE-VIDA'),
    ('mundo', 'MUNDO'),
    ('utilidades','UTILIDADES'),
    ('cocina','COCINA'),
    ('tutoriales','TUTORIALES'),
    ('bloguer','BLOGUER'),
    ('cultura','CULTURA'),
    ('negocios','NEGOCIOS'),
    ('politica','POLITICA'),
    ('opinion','OPINION'),
    ('moda', 'MODA'),
    ('viajes','VIAJES'),

)


class Post(models.Model):
    id_post=models.AutoField(primary_key=True, auto_created = True)
    titulo=models.CharField(max_length=100,help_text="Título del artículo")
    descripcion=models.CharField(max_length=300,help_text="Descripción corta del artículo", default="", null=True, blank=True)
    articulo=models.TextField(help_text="Escriba aquí su artículo")
    imagen_principal=models.ImageField(upload_to='posts/images',help_text="Imágen principal")
    autor=models.ForeignKey(Porfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    publicado=models.BooleanField(default=False)
    categoria=models.CharField(max_length=20,help_text="Categoria del artículo", default="bloguer", choices=CHOICES)
    visitas=models.IntegerField(default=0)




    class Meta:
        verbose_name_plural = "Posts"

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
        verbose_name_plural = "PostGuardados"

    def __str__(self):
        return f"Guardado el post con fecha: {self.guardado_el}"
