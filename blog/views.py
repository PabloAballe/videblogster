from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
import datetime
from .models import Porfile
from .models import PostGuardado
from .models import Post
from .models import Comentario
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
from django.contrib.auth.models import User
from .models  import *
from django.contrib import messages
from django.views.defaults import page_not_found
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django_email_verification import send_email
from .forms import AFWithEmail,UCFWithEmail
import requests
from datetime import datetime as time

def handler_404(request, exception):
    return page_not_found(request, exception, template_name="404.html")

def ads_txt(request):
   return render(request, 'ads.txt',{})



def no_existe(request):
    if request.method == "POST":
        form = SheachForm(request.POST)

        if form.is_valid():
            q= form.cleaned_data['shearch']
            existe=Post.objects.all().order_by('-id_post').filter(articulo__contains=q).exists()
            if existe==True:
                post_all=Post.objects.all().order_by('-id_post').filter(articulo__contains=q)
            else:
                return redirect("no_existe")
            primer_post=False
    else:
        form = SheachForm()

    categoria=Post.objects.all().order_by('-visitas')[:5]
    context={ 'form': form, 'categoria': categoria}
    return render(request, "no_existe.html", context)


def home(request, msg=""):
    # data = dict()
    # messages.success(request, "Success: This is the sample success Flash message.")
    # messages.error(request, "Error: This is the sample error Flash message.")
    # messages.info(request, "Info: This is the sample info Flash message.")
    # messages.warning(request, "Warning: This is the sample warning Flash message.")
    date=datetime.date.today().day
    now = time.now()
    post=Post.objects.all().order_by('-id_post')[:10]
    primer_post=Post.objects.all().order_by('-id_post').first()
    post_all=Post.objects.all().order_by('-id_post')[1:100]
    total=Post.objects.all().aggregate(sum=Sum('visitas'))
    categoria=Post.objects.all().order_by('-visitas')[:5]
    categorias=Categorias.objects.all().order_by('-categoria_nombre')

#set 0 because begueans the mont
    # if date==1 and now.time=='00:00:00':
    #     vistas=Porfile.objects.all()
    #     vistas.update(vistas=0)
    #     visitas=Post.objects.all()
    #     visitas.update(visitas=0)

    if request.method == "POST":
        form = SheachForm(request.POST)

        if form.is_valid():
            q= form.cleaned_data['shearch']
            existe=Post.objects.all().order_by('-id_post').filter(articulo__contains=q).exists()
            if existe==True:
                post_all=Post.objects.all().order_by('-id_post').filter(articulo__contains=q)
            else:
                return redirect("no_existe")
            primer_post=False
    else:
        form = SheachForm()


    context={"date": date, "post": post, 'primer_post': primer_post, 'post_all': post_all, 'form': form, 'total': total, 'categoria': categoria, 'categorias':categorias}

    return render(request, 'home.html', context)

@login_required
def porfile(request):
    user=request.user
    seguidores=Seguidores.objects.all().filter(sigue=user.pk)
    seguidos=Seguidores.objects.all().filter(seguido=user.pk)
    num_seguidores=seguidores.count()
    num_seguidos=seguidos.count()
    porfile=get_object_or_404(Porfile, pk=user.porfile.pk)
    posts=Post.objects.all().filter(autor=user.porfile).order_by('-id_post')
    post_count=posts.count()
    count=Post.objects.all().filter(autor=user.porfile,publicado=True).count()
    porfile.total_post=count
    porfile.save()
    categoria=Post.objects.all().order_by('-visitas')[:5]
    context={ 'categoria': categoria, 'porfile': porfile, 'user': user, 'posts': posts, 'post_count': post_count, 'num_seguidores': num_seguidores, 'num_seguidos': num_seguidos}
    return render(request, 'porfile.html', context)

def top(request):
    if request.method == "POST":
        form = SheachForm(request.POST)

        if form.is_valid():
            q= form.cleaned_data['shearch']
            existe=Post.objects.all().order_by('-id_post').filter(articulo__contains=q).exists()
            if existe==True:
                post_all=Post.objects.all().order_by('-id_post').filter(articulo__contains=q)
            else:
                return redirect("no_existe")
            primer_post=False
    else:
        form = SheachForm()

    categoria=Post.objects.all().order_by('-visitas')[:5]
    post=Post.objects.all().order_by('-visitas')[:100]



    context={'categoria': categoria, 'form': form,'post': post }
    return render(request, 'top.html', context)


def post_details(request, pk):
    post=Post.objects.all().order_by('-id_post')[:10]
    post_details = get_object_or_404(Post, pk=pk)
    comment_form  = ComentarioForm()
    anonimus=request.user
    actual_user=None
    guardado=False
    categorias=Categorias.objects.all().order_by('-categoria_nombre')

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

    if request.method == "POST":
        form = SheachForm(request.POST)

        if form.is_valid():
            q= form.cleaned_data['shearch']
            existe=Post.objects.all().order_by('-id_post').filter(articulo__contains=q).exists()
            if existe==True:
                post_all=Post.objects.all().order_by('-id_post').filter(articulo__contains=q)
            else:
                return redirect("no_existe")
            primer_post=False
    else:
        form = SheachForm()



    categoria=Post.objects.all().order_by('-visitas')[:5]
    post_details.visitas=post_details.visitas+1
    post_details.save()
    porfile=get_object_or_404(Porfile, usuario=post_details.autor.usuario  )
    porfile.vistas=porfile.vistas+1
    porfile.save()
    context={'post_details': post_details, 'porfile': porfile, 'form': form, 'categoria': categoria, 'comment_form': comment_form, 'comentarios': comentarios, 'comentario': comentario,'actual_user': actual_user, 'guardado': guardado, 'post': post, 'categorias':categorias}
    return render(request, 'post_details.html', context)


def guardar_post(request, pk):
    user=request.user
    post = get_object_or_404(Post, pk=pk)
    guardar=PostGuardado.objects.create(usuario=user, post=post)
    guardar.save()
    msg="Se ha guardado correctamente el post"
    return redirect('post_guardados');

def post_guardados(request):
    user=request.user
    post_guardados=PostGuardado.objects.all().filter(usuario=user).order_by('-id_post_guardado')
    return render(request, 'post_guardados.html',{'post': post_guardados})

def guardado_quit(request, pk):
    user=request.user
    borrar_post_guardado=get_object_or_404(PostGuardado, post=pk, usuario=user).delete()
    return redirect("post_guardados")


def categoria(request, pk):
    categorias=Categorias.objects.all().order_by('-categoria_nombre')
    cat=Post.objects.all().order_by('-visitas').filter(categoria=pk)[:100]
    context={'categorias': categorias, 'post_all': cat}
    return render(request, 'categoria_details.html', context)


def register(request):
    categoria=Post.objects.all().order_by('-visitas')[:5]
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


def login(request):
    categoria=Post.objects.all().order_by('-visitas')[:5]
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

def logout(request):
     do_logout(request)
     return redirect('home')

def post_new(request):
    porfile=Porfile.objects.get(usuario=request.user)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES,instance=request.user)
        if form.is_valid():
            post = form.save()
            titulo=form.cleaned_data['titulo']
            descripcion=form.cleaned_data['descripcion']
            articulo=form.cleaned_data['articulo']
            categoria=form.cleaned_data['categoria']
            autor = porfile
            imagen_principal=form.cleaned_data['imagen_principal']
            articulo= Post.objects.create(titulo=titulo,    descripcion=descripcion ,articulo=articulo,categoria=categoria, autor=autor, imagen_principal=imagen_principal  )
            post.save()
            return redirect('porfile')
    else:
        form = PostForm()
    return render(request, 'post_edit.html', {'form': form})


def delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    context= {'post': post}
    return render(request, 'delete.html', context)

def delete_com(request, pk):
    coment = get_object_or_404(Comentario, pk=pk)
    post=coment.post_comentario.pk
    com = get_object_or_404(Comentario, pk=pk).delete()
    context= {'com': com}
    return redirect('post_details', pk=post)

def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk).delete()
    return redirect("porfile")


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


def privacy(request):
    return render(request, 'privacy.html')

def faq(request):
    year=datetime.date.today().year
    return render(request, 'faq.html',{'year': year})


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

def view_porfile(request ,pk):
    sigue=Seguidores.objects.all().filter(sigue=request.user).exists()
    esta_siguiendo=False
    if sigue==True:
        esta_siguiendo=True
    user=get_object_or_404(Porfile, id_porfile=pk)
    posts=Post.objects.all().filter(autor=user).order_by('-id_post')
    post_count=posts.count()
    return render(request, 'view_porfile.html',{'user': user, 'posts': posts,'post_count': post_count, 'esta_siguiendo': esta_siguiendo})


def seguir(request, pk):
    other_user = get_object_or_404(User,pk=pk)
    s=Seguidores(sigue=request.user, seguido=other_user)
    s.save()
    return redirect('porfile')

def dejar_seguir(request, pk):
    other_user = get_object_or_404(User,pk=pk)
    get_object_or_404(Seguidores,seguido=other_user, sigue=request.user).delete()
    return redirect('porfile')

def siguiendo(request,pk):
    user=request.user
    seguidos=Seguidores.objects.all().filter(sigue=user)
    return render(request, 'siguiendo.html',{'users': seguidos})

def seguidores(request,pk):
    user=request.user
    seguidores=Seguidores.objects.all().filter(seguido=user)
    return render (request, 'seguidores.html', {'users': seguidores})

def api_download(request):
    apikey="e83329a486a64c37853186467a6d63b7"
    date=datetime.date.today().day
    now = time.now()
    top = requests.get(f"https://newsapi.org/v2/top-headlines?language=es&apiKey={apikey}").json()  
    espana = requests.get(f"https://newsapi.org/v2/everything?q=espa%C3%B1a&apiKey={apikey}").json() 
    eua = requests.get(f"https://newsapi.org/v2/everything?q=eua&language=es&apiKey={apikey}").json() 
    bitcoin = requests.get(f"https://newsapi.org/v2/everything?q=bitcoin&language=es&apiKey={apikey}").json() 
    tecnologia = requests.get(f"https://newsapi.org/v2/everything?q=tecnologia&language=es&apiKey={apikey}").json()
    mundo = requests.get(f"https://newsapi.org/v2/everything?q=mundo&language=es&apiKey={apikey}").json() 
    moda = requests.get(f"https://newsapi.org/v2/everything?q=moda&language=es&apiKey={apikey}").json()
    tutoriales = requests.get(f"https://newsapi.org/v2/everything?q=tutoriales&language=es&apiKey={apikey}").json()
    ciencia = requests.get(f"https://newsapi.org/v2/everything?q=ciencia&language=es&apiKey={apikey}").json()
    cine = requests.get(f"https://newsapi.org/v2/everything?q=cine&language=es&apiKey={apikey}").json()
    negocios = requests.get(f"https://newsapi.org/v2/everything?q=negocios&language=es&apiKey={apikey}").json()
    politica = requests.get(f"https://newsapi.org/v2/everything?q=politica&language=es&apiKey={apikey}").json()
    salud = requests.get(f"https://newsapi.org/v2/everything?q=salud&language=es&apiKey={apikey}").json()
    deportes = requests.get(f"https://newsapi.org/v2/everything?q=deportes&language=es&apiKey={apikey}").json()
    opinion = requests.get(f"https://newsapi.org/v2/everything?q=opinion&language=es&apiKey={apikey}").json()
    viajes = requests.get(f"https://newsapi.org/v2/everything?q=viajes&language=es&apiKey={apikey}").json()
    categoria_top=Categorias.objects.all()[0]
    categoria_espana=Categorias.objects.all()[1]
    categoria_eua=Categorias.objects.all()[2]
    categoria_bitcoin=Categorias.objects.all()[3]
    categoria_tecnologia=Categorias.objects.all()[4]
    categoria_mundo=Categorias.objects.all()[5]
    categoria_moda=Categorias.objects.all()[6]
    categoria_tutoriales=Categorias.objects.all()[7]
    categoria_ciencia=Categorias.objects.all()[8]
    categoria_cine=Categorias.objects.all()[9]
    categoria_negocios=Categorias.objects.all()[10]
    categoria_politica=Categorias.objects.all()[11]
    categoria_salud=Categorias.objects.all()[12]
    categoria_deportes=Categorias.objects.all()[13]
    categoria_opinion=Categorias.objects.all()[14]
    categoria_viajes=Categorias.objects.all()[15]
    for post in top['articles']:
        p=Post(titulo=post['title'], descripcion=post['description'], articulo=str(post['content'])+'\n'+'Autor: '+str(post['author'])+'\n'+'Seguir leyendo: '+str(post['url']),imagen_url=post['urlToImage'],autor=request.user.porfile, publicado=True,categoria=categoria_top , created_at=post['publishedAt'])
        p.save()
    for post in espana['articles']:
        p=Post(titulo=post['title'], descripcion=post['description'], articulo=str(post['content'])+'\n'+'Autor: '+str(post['author'])+'\n'+'Seguir leyendo: '+str(post['url']),imagen_url=post['urlToImage'],autor=request.user.porfile, publicado=True,categoria=categoria_espana , created_at=post['publishedAt'])
        p.save()
    for post in eua['articles']:
        p=Post(titulo=post['title'], descripcion=post['description'], articulo=str(post['content'])+'\n'+'Autor: '+str(post['author'])+'\n'+'Seguir leyendo: '+str(post['url']),imagen_url=post['urlToImage'],autor=request.user.porfile, publicado=True,categoria=categoria_eua , created_at=post['publishedAt'])
        p.save()
    for post in bitcoin['articles']:
        p=Post(titulo=post['title'], descripcion=post['description'], articulo=str(post['content'])+'\n'+'Autor: '+str(post['author'])+'\n'+'Seguir leyendo: '+str(post['url']),imagen_url=post['urlToImage'],autor=request.user.porfile, publicado=True,categoria=categoria_bitcoin , created_at=post['publishedAt'])
        p.save()
    for post in tecnologia['articles']:
        p=Post(titulo=post['title'], descripcion=post['description'], articulo=str(post['content'])+'\n'+'Autor: '+str(post['author'])+'\n'+'Seguir leyendo: '+str(post['url']),imagen_url=post['urlToImage'],autor=request.user.porfile, publicado=True,categoria=categoria_tecnologia , created_at=post['publishedAt'])
        p.save()
    for post in mundo['articles']:
        p=Post(titulo=post['title'], descripcion=post['description'], articulo=str(post['content'])+'\n'+'Autor: '+str(post['author'])+'\n'+'Seguir leyendo: '+str(post['url']),imagen_url=post['urlToImage'],autor=request.user.porfile, publicado=True,categoria=categoria_mundo , created_at=post['publishedAt'])
        p.save()
    for post in moda['articles']:
        p=Post(titulo=post['title'], descripcion=post['description'], articulo=str(post['content'])+'\n'+'Autor: '+str(post['author'])+'\n'+'Seguir leyendo: '+str(post['url']),imagen_url=post['urlToImage'],autor=request.user.porfile, publicado=True,categoria=categoria_moda , created_at=post['publishedAt'])
        p.save()
    for post in tutoriales['articles']:
        p=Post(titulo=post['title'], descripcion=post['description'], articulo=str(post['content'])+'\n'+'Autor: '+str(post['author'])+'\n'+'Seguir leyendo: '+str(post['url']),imagen_url=post['urlToImage'],autor=request.user.porfile, publicado=True,categoria=categoria_tutoriales , created_at=post['publishedAt'])
        p.save()
    for post in ciencia['articles']:
        p=Post(titulo=post['title'], descripcion=post['description'], articulo=str(post['content'])+'\n'+'Autor: '+str(post['author'])+'\n'+'Seguir leyendo: '+str(post['url']),imagen_url=post['urlToImage'],autor=request.user.porfile, publicado=True,categoria=categoria_ciencia , created_at=post['publishedAt'])
        p.save()
    for post in cine['articles']:
        p=Post(titulo=post['title'], descripcion=post['description'], articulo=str(post['content'])+'\n'+'Autor: '+str(post['author'])+'\n'+'Seguir leyendo: '+str(post['url']),imagen_url=post['urlToImage'],autor=request.user.porfile, publicado=True,categoria=categoria_cine , created_at=post['publishedAt'])
        p.save()
    for post in negocios['articles']:
        p=Post(titulo=post['title'], descripcion=post['description'], articulo=str(post['content'])+'\n'+'Autor: '+str(post['author'])+'\n'+'Seguir leyendo: '+str(post['url']),imagen_url=post['urlToImage'],autor=request.user.porfile, publicado=True,categoria=categoria_negocios , created_at=post['publishedAt'])
        p.save()
    for post in politica['articles']:
        p=Post(titulo=post['title'], descripcion=post['description'], articulo=str(post['content'])+'\n'+'Autor: '+str(post['author'])+'\n'+'Seguir leyendo: '+str(post['url']),imagen_url=post['urlToImage'],autor=request.user.porfile, publicado=True,categoria=categoria_politica , created_at=post['publishedAt'])
        p.save()
    for post in salud['articles']:
        p=Post(titulo=post['title'], descripcion=post['description'], articulo=str(post['content'])+'\n'+'Autor: '+str(post['author'])+'\n'+'Seguir leyendo: '+str(post['url']),imagen_url=post['urlToImage'],autor=request.user.porfile, publicado=True,categoria=categoria_salud , created_at=post['publishedAt'])
        p.save()
    for post in deportes['articles']:
        p=Post(titulo=post['title'], descripcion=post['description'], articulo=str(post['content'])+'\n'+'Autor: '+str(post['author'])+'\n'+'Seguir leyendo: '+str(post['url']),imagen_url=post['urlToImage'],autor=request.user.porfile, publicado=True,categoria=categoria_deportes , created_at=post['publishedAt'])
        p.save()
    for post in opinion['articles']:
        p=Post(titulo=post['title'], descripcion=post['description'], articulo=str(post['content'])+'\n'+'Autor: '+str(post['author'])+'\n'+'Seguir leyendo: '+str(post['url']),imagen_url=post['urlToImage'],autor=request.user.porfile, publicado=True,categoria=categoria_opinion , created_at=post['publishedAt'])
        p.save()
    for post in viajes['articles']:
        p=Post(titulo=post['title'], descripcion=post['description'], articulo=str(post['content'])+'\n'+'Autor: '+str(post['author'])+'\n'+'Seguir leyendo: '+str(post['url']),imagen_url=post['urlToImage'],autor=request.user.porfile, publicado=True,categoria=categoria_viajes , created_at=post['publishedAt'])
        p.save()
    return redirect('porfile')
