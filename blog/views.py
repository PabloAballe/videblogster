from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
import datetime
from .forms import SheachForm
from django.contrib.auth import logout as do_logout
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login
from django.db.models import Sum
from .forms import ComentarioForm
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from .forms import PorfileForm
from django.contrib.auth.models import User
from .forms import UserForm
from annoying.functions import get_object_or_None
from .models  import *
from django.contrib import messages
from django.views.defaults import page_not_found
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django_email_verification import send_email
from .forms import AFWithEmail,UCFWithEmail
import requests
from datetime import datetime as time
from youtube_search import YoutubeSearch
import json
from django.http import HttpResponse
import youtube_dl
from django.contrib import messages
from django.http import FileResponse
from django.core.files.base import ContentFile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from youtubesearchpython import VideosSearch
from youtubesearchpython import *
import json
from django.http import JsonResponse
from asgiref.sync import sync_to_async
#youtube downloader
from pytube import *
import os, glob
import mimetypes
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import hashlib # A standard library that does hashes
from django.conf import settings
# Mailchimp Settings
api_key = settings.MAILCHIMP_API_KEY
server = settings.MAILCHIMP_DATA_CENTER
list_id = settings.MAILCHIMP_EMAIL_LIST_ID

from django.conf import settings
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMessage

# Email Logic
@sync_to_async
@login_required
def send_email(request):
    sender = settings.EMAIL_HOST_USER.encode(encoding='utf-8')
    post_all=Post.objects.all().order_by('?')[:10]
    emails = User.objects.filter(is_active=True).exclude(email='').values_list('email', flat=True)
    msg_html = render_to_string('mails_from_users.html', {
        'post_all': post_all
    })
    to_list='pablo970616@gmail.com'
    msg = EmailMessage(subject='Novedades en Video Blosgter 😉', body=msg_html, from_email=sender, bcc=[to_list])
    msg.content_subtype = "html"  # Main content is now text/html
    return msg.send()


@sync_to_async
def handler_404(request, exception):
    return page_not_found(request, exception, template_name="404.html")
@sync_to_async
def ads_txt(request):
   return render(request, 'ads.txt',{})


@sync_to_async
def no_existe(request):
    return render(request, "no_existe.html")

@sync_to_async
def home(request, msg=""):
    # data = dict()
    # messages.success(request, "Success: This is the sample success Flash message.")
    # messages.error(request, "Error: This is the sample error Flash message.")
    # messages.info(request, "Info: This is the sample info Flash message.")
    # messages.warning(request, "Warning: This is the sample warning Flash message.")
    usuarios=Porfile.objects.all().order_by('?')[:6]
    date=datetime.date.today().day
    now = time.now()
    post=Post.objects.all().order_by('-visitas')[:10]
    primer_post=Post.objects.all().order_by('-visitas').first()
    post_all=Post.objects.all().order_by('?')[1:25]
    categoria=Post.objects.all().order_by('-visitas').distinct()[:10]
    categorias=Categorias.objects.all().order_by('?')[:10]



    if request.method == "POST":
        form = SheachForm(request.POST)

        if form.is_valid():
            q= form.cleaned_data['shearch'].lower()
            existe=Post.objects.all().order_by('-id_post').filter(titulo__icontains=q  ).exists()
            if existe==True:
                post_all=Post.objects.all().order_by('-id_post').filter(titulo__icontains=q  )
            else:
                return redirect("no_existe")
            primer_post=False
    else:
        form = SheachForm()


    context={"date": date, "post": post, 'primer_post': primer_post, 'post_all': post_all, 'form': form, 'categoria': categoria, 'categorias':categorias, 'usuarios': usuarios}

    return render(request, 'home.html', context)
@sync_to_async
@login_required
def porfile(request):
    user=request.user
    seguidores=Seguidores.objects.all().filter(sigue=user.pk)
    seguidos=Seguidores.objects.all().filter(seguido=user.pk)
    num_seguidores=seguidores.count()
    num_seguidos=seguidos.count()
    porfile=get_object_or_404(Porfile, pk=user.porfile.pk)
    posts=Post.objects.all().filter(autor=user.porfile).order_by('-id_post')[:100]
    post_count=posts.count()
    count=Post.objects.all().filter(autor=user.porfile,publicado=True).count()
    porfile.total_post=count
    porfile.save()
    categoria=Post.objects.all().order_by('-visitas')[:5]
    context={ 'categoria': categoria, 'porfile': porfile, 'user': user, 'posts': posts, 'post_count': post_count, 'num_seguidores': num_seguidores, 'num_seguidos': num_seguidos}
    return render(request, 'porfile.html', context)
@sync_to_async
def top(request):
    categoria=Post.objects.all().order_by('-visitas')[:10]
    categorias=Categorias.objects.all().order_by('?')[:10]
    post=Post.objects.all().order_by('-visitas')[:100]
    if request.method == "POST":
        form = SheachForm(request.POST)

        if form.is_valid():
            q= form.cleaned_data['shearch'].lower()
            existe=Post.objects.all().order_by('-id_post').filter(titulo__icontains=q  ).exists()
            if existe==True:
                post=Post.objects.all().order_by('-id_post').filter(titulo__icontains=q  )
            else:
                return redirect("no_existe")
            primer_post=False
    else:
        form = SheachForm()


    context={'categoria': categoria,'categorias': categorias, 'form': form,'post': post }
    return render(request, 'top.html', context)

@sync_to_async
def post_details(request, pk):
    post=Post.objects.all().order_by('?')[:15]
    post_details = get_object_or_404(Post, pk=pk)
    comment_form  = ComentarioForm()
    anonimus=request.user
    actual_user=None
    guardado=False
    liked_post_check=False
    categorias=Categorias.objects.all().order_by('?')[:10]
    if anonimus.id != None:
        actual_user=request.user
        post_guardado = get_object_or_None(PostGuardado, post=pk, usuario=request.user)

        porfile=Porfile.objects.get(usuario=request.user)

        if post_guardado!=None:
            guardado=True

    comentario = None
    comentarios = Comentario.objects.all().filter(post_comentario=pk).order_by('-pk')
    comment_form = ComentarioForm()
    if comentario==None:
        if request.POST:
            comment_form = ComentarioForm(request.POST,instance=request.user)

            if comment_form.is_valid():
                comment  = comment_form.save()
                comentario_cl = comment_form.cleaned_data['comentario']
                comment.comentario=comentario_cl
                post_comentario=post_details
                autor_comentario=request.user
                comentario = Comentario.objects.create(comentario=comentario_cl,    post_comentario=post_details
                ,author_comentario=porfile )
                comment_form.save()
                comentario=True
                return redirect("post_details", pk=post_details.pk )

            else:
                comment_form  = ComentarioForm()




    categoria=Post.objects.all().order_by('-visitas')[:10]
    post_details.visitas=post_details.visitas+1
    post_details.save()
    porfile=get_object_or_404(Porfile, usuario=post_details.autor.usuario  )
    porfile.vistas=porfile.vistas+1
    porfile.save()
    context={'post_details': post_details, 'porfile': porfile, 'categoria': categoria, 'comment_form': comment_form, 'comentarios': comentarios, 'comentario': comentario,'actual_user': actual_user, 'guardado': guardado, 'post': post, 'categorias':categorias}
    return render(request, 'post_details.html', context)
@sync_to_async
@login_required
def guardar_post(request, pk):
    user=request.user
    post = get_object_or_404(Post, pk=pk)
    guardar=PostGuardado.objects.create(usuario=user, post=post)
    guardar.save()
    msg="Se ha guardado correctamente el post"
    return redirect('post_guardados')
@sync_to_async
@login_required
def post_guardados(request):
    user=request.user
    post_guardados=PostGuardado.objects.all().filter(usuario=user).order_by('-id_post_guardado')
    return render(request, 'post_guardados.html',{'post': post_guardados})
@sync_to_async
@login_required
def guardado_quit(request, pk):
    user=request.user
    borrar_post_guardado=get_object_or_404(PostGuardado, post=pk, usuario=user).delete()
    return redirect("post_guardados")

@sync_to_async
def categoria(request, pk):
    categorias=Categorias.objects.all().order_by('?')[:10]
    cate=Post.objects.all().order_by('-visitas').filter(categoria=pk)[:80]
    categoria=Post.objects.all().order_by('-visitas')[:10]
    page = request.GET.get('page', 1)

    paginator = Paginator(cate, 10)
    try:
        cat = paginator.page(page)
    except PageNotAnInteger:
        cat = paginator.page(1)
    except EmptyPage:
        cat = paginator.page(paginator.num_pages)

    if request.method == "POST":
        form = SheachForm(request.POST)

        if form.is_valid():
            q= form.cleaned_data['shearch'].lower()
            existe=Post.objects.all().order_by('-id_post').filter(titulo__icontains=q, categoria=pk ).exists()
            if existe==True:
                cat=Post.objects.all().order_by('-id_post').filter(titulo__icontains=q,categoria=pk)
            else:
                return redirect("no_existe")
            primer_post=False
    else:
        form = SheachForm()
    context={'categorias': categorias, 'post_all': cat, 'categoria': categoria , 'form': form }
    return render(request, 'categoria_details.html', context)

@sync_to_async
def register(request):
    categoria=Post.objects.all().order_by('-visitas')[:10]
    # Creamos el formulario de autenticación vacío
    form_reg = UCFWithEmail()



    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form_reg = UCFWithEmail(data=request.POST)

        # Si el formulario es válido...
        if form_reg.is_valid():

            # Creamos la nueva cuenta de usuario
            user = form_reg.save()
            # Si el usuario se crea correctamente
            if user is not None:
                # Hacemos el login manualmente
                do_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                # Y le redireccionamos a la portada
                user.is_active = False
                #user.email=user.username  # Example
                send_email(user, fail_silently=False)
                return redirect('/')


    # Si llegamos al final renderizamos el formulario
    return render(request, "register.html", {'form_reg': form_reg, 'categoria': categoria})

@sync_to_async
def login(request):
    categoria=Post.objects.all().order_by('-visitas')[:10]
    # Creamos el formulario de autenticación vacío
    form_auth = AFWithEmail()
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form_auth = AFWithEmail(data=request.POST)
        # Si el formulario es válido...
        if form_auth.is_valid():
            # Recuperamos las credenciales validadas
            username = form_auth.cleaned_data['username']
            password = form_auth.cleaned_data['password']

            # Verificamos las credenciales del usuario
            user = authenticate(username=username, password=password)

            # Si existe un usuario con ese nombre y contraseña
            if user is not None:
                # Hacemos el login manualmente
                do_login(request, user, backend='allauth.account.auth_backends.AuthenticationBackend')
                # Y le redireccionamos a la portada
                return redirect('/')

    # Si llegamos al final renderizamos el formulario
    return render(request, "login.html", {'form_auth': form_auth, 'categoria':categoria })
@sync_to_async
@login_required
def logout(request):
     do_logout(request)
     return redirect('home')
@sync_to_async
@login_required
def post_new(request):
    porfile=Porfile.objects.get(usuario=request.user)
    if request.method == "POST":

        form = PostForm(request.POST, request.FILES,instance=request.user)

        if form.is_valid():
            post = form.save()
            titulo=form.cleaned_data['titulo']
            descripcion=form.cleaned_data['descripcion']

            categoria=form.cleaned_data['categoria']
            autor = porfile
            imagen_principal=form.cleaned_data['imagen_principal']
            video=form.cleaned_data['video']
            articulo= Post.objects.create(titulo=titulo,    descripcion=descripcion ,video=video,categoria=categoria, autor=autor, imagen_principal=imagen_principal  )
            post.save()
            return redirect('porfile')
    else:
        form = PostForm()
    return render(request, 'post_edit.html', {'form': form})

@sync_to_async
@login_required
def delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    context= {'post': post}
    return render(request, 'delete.html', context)
@login_required
@sync_to_async
def delete_com(request, pk):
    coment = get_object_or_404(Comentario, pk=pk)
    post=coment.post_comentario.pk
    com = get_object_or_404(Comentario, pk=pk).delete()
    context= {'com': com}
    return redirect('post_details', pk=post)
@sync_to_async
@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk).delete()
    return redirect("porfile")
@sync_to_async
@login_required
def post_edit(request, pk):
    porfile=Porfile.objects.get(usuario=request.user)
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES,instance=post)
        if form.is_valid():
            post = form.save()
            titulo=form.cleaned_data['titulo']
            descripcion=form.cleaned_data['descripcion']
            articulo=form.cleaned_data['articulo']
            categoria=form.cleaned_data['categoria']
            autor = porfile
            imagen_principal=form.cleaned_data['imagen_principal']
            # articulo= Post.objects.create(titulo=titulo,    descripcion=descripcion ,articulo=articulo,categoria=categoria, autor=autor, imagen_principal=imagen_principal  )
            post.save()
            return redirect('post_details', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'post_edit.html', {'form': form})

@sync_to_async
def privacy(request):
    return render(request, 'privacy.html')
@sync_to_async
def faq(request):
    year=datetime.date.today().year
    condiciones=Condicion.objects.all()
    return render(request, 'faq.html',{'year': year,'condiciones': condiciones})

@sync_to_async
@login_required
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = PorfileForm(request.POST, request.FILES, instance=request.user.porfile )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('porfile')
        else:
            pass
    else:
        user_form = UserForm(instance=request.user)
        profile_form = PorfileForm(instance=request.user.porfile)
    return render(request, 'edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
@sync_to_async
@login_required
def view_porfile(request ,pk):
    user_seguido=get_object_or_404(Porfile, id_porfile=pk)
    sigue=Seguidores.objects.all().filter(sigue=request.user, seguido=user_seguido.usuario).exists()
    esta_siguiendo=False
    if sigue==True:
        esta_siguiendo=True
    user=get_object_or_404(Porfile, id_porfile=pk)
    posts=Post.objects.all().filter(autor=user).order_by('-id_post')[:100]
    post_count=posts.count()
    return render(request, 'view_porfile.html',{'user': user, 'posts': posts,'post_count': post_count, 'esta_siguiendo': esta_siguiendo})
@sync_to_async
@login_required
def seguir(request, pk):
    other_user = get_object_or_404(User,pk=pk)
    s=Seguidores(sigue=request.user, seguido=other_user)
    s.save()
    return redirect('porfile')
@sync_to_async
@login_required
def dejar_seguir(request, pk):
    other_user = get_object_or_404(User,pk=pk)
    get_object_or_404(Seguidores,seguido=other_user, sigue=request.user).delete()
    return redirect('porfile')
@sync_to_async
@login_required
def siguiendo(request,pk):
    user=request.user
    seguidos=Seguidores.objects.all().filter(sigue=user)
    return render(request, 'siguiendo.html',{'users': seguidos})
@login_required
def seguidores(request,pk):
    user=request.user
    seguidores=Seguidores.objects.all().filter(seguido=user)
    return render (request, 'seguidores.html', {'users': seguidores})



    return redirect('porfile')
@sync_to_async
@login_required
def like_post(request, pk):
    user=request.user
    post = get_object_or_404(Post, pk=pk)
    guardar=PostLike.objects.create(usuario=user, post=post)
    guardar.save()
    return redirect('liked_post')
@sync_to_async
@login_required
def liked_post(request):
    user=request.user
    post_guardados=PostLike.objects.all().filter(usuario=user).order_by('-id_post_like')
    return render(request, 'liked_post.html',{'post': liked_post})
@sync_to_async
@login_required
def like_quit(request, pk):
    user=request.user
    borrar_post_guardado=get_object_or_404(PostLike, post=pk, usuario=user).delete()
    return redirect("liked_post")

#descargar video
@sync_to_async
def downloadvideo(request):
     # checking wheather request.method is post or not
    if request.method == 'POST':
        videourl = request.POST['url']
        validate = URLValidator()
        try:
            validate(videourl)
            video= YouTube(videourl)
            videoHD=video.streams.get_highest_resolution()
            directory_path = os.getcwd()
            module_dir = os.path.dirname(__file__)
            filename ='video'
            file_path = os.path.join(module_dir, filename)
            try:
                videoHD.download(f"{module_dir}", filename)
            except:
                messages.warning(request, 'El video seleccionado no permite desacargas por derechos de contenidos')
                return redirect("home")
            try:
              with open(f'{module_dir}/{filename}.mp4', 'rb') as fl:
                mime_type, _ = mimetypes.guess_type(file_path)
                response = HttpResponse(fl, content_type=mime_type)
                response['Content-Disposition'] = "attachment; filename=%s" % f'{filename}.mp4'
                messages.success(request, 'Video descargado.')
                return response
            except FileNotFoundError:
                messages.warning(request, 'No se ha podido guardar el video')
                return redirect("home")
        except ValidationError:
            messages.warning(request, 'Porfavor ingrese una url válida')
            return redirect("home")
    return redirect("home")

#descargar video
@sync_to_async
def downloadvideourl(request, pk):
     # checking wheather request.method is post or not
    if request.method == 'POST':
        videourl = request.POST['url']

        try:
            video= YouTube(videourl)
            videoHD=video.streams.get_highest_resolution()
            directory_path = os.getcwd()
            module_dir = os.path.dirname(__file__)
            filename ='video'
            file_path = f'{module_dir}/{filename}.mp4'
            videoHD.download(f"{module_dir}", filename)
            try:
                with open( f'{module_dir}/{filename}', 'rb') as fl:
                    mime_type, _ = mimetypes.guess_type(file_path)
                    response = HttpResponse(fl, content_type=mime_type)
                    response['Content-Disposition'] = "attachment; filename=%s" % f'{filename}.mp4'
                    messages.success(request, 'Video descargado.')
                    return response
            except FileNotFoundError:
                messages.warning(request, 'No se ha podido descargar el video')
                return redirect("post_details", pk=pk)
        except:
            messages.warning(request, 'El video seleccionado no permite desacargas por derechos de contenidos')
            return redirect("home")

    return redirect("post_details", pk=pk)

#descargar video
@sync_to_async
def downloadaudiourl(request, pk):
     # checking wheather request.method is post or not
    if request.method == 'POST':
        videourl = request.POST['url']
        try:
            video= YouTube(videourl)
            videoHD=video.streams.filter(type = "audio").first()
            directory_path = os.getcwd()
            module_dir = os.path.dirname(__file__)
            filename ='audio'
            file_path = f'{module_dir}/{filename}.mp4'
            videoHD.download(f"{module_dir}", filename)
            try:
                with open( f'{module_dir}/{filename}', 'rb') as fl:
                 mime_type, _ = mimetypes.guess_type(file_path)
                 response = HttpResponse(fl, content_type=mime_type)
                 response['Content-Disposition'] = "attachment; filename=%s" % f'{filename}.mp4'
                 return response
                    #return HttpResponse( f'{module_dir}/{filename}')
            except FileNotFoundError:
                messages.warning(request, 'No se ha encontrado el archivo')
                return redirect("post_details", pk=pk)
        except:
            messages.warning(request, 'El video seleccionado no permite desacargas por derechos de contenidos')
            return redirect("home")

    return redirect("post_details", pk=pk)


@login_required
def api_download(request):
    apikey="e83329a486a64c37853186467a6d63b7"
    date=datetime.date.today().day
    now = time.now()
    categorias=Categorias.objects.all()
    for categorias in categorias:
        try:
            req = YoutubeSearch(categorias.categoria_api, max_results=10000).to_json()
            data = json.loads(req)
            for post in data["videos"]:
                try:
                    p=Post(titulo=post['title'], descripcion=post['long_desc'], video_url=post['id'],imagen_url=post['thumbnails'][0],autor=request.user.porfile, publicado=True,categoria=categorias )
                    p.save()
                except:
                    pass
        except:
            pass


    return redirect('porfile')


