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

    categoria=Post.objects.all().order_by('-visitas')[:10]
    context={ 'form': form, 'categoria': categoria}
    return render(request, "no_existe.html", context)


def home(request):
    date=datetime.date.today().day
    post=Post.objects.all().order_by('-id_post')[:10]
    primer_post=Post.objects.all().order_by('-id_post').first()
    post_all=Post.objects.all().order_by('-id_post')[:100]
    total=Post.objects.all().aggregate(sum=Sum('visitas'))
    categoria=Post.objects.all().order_by('-visitas')[:10]

#set 0 because begueans the mont
    if date==1:
        vistas=Porfile.objects.all()
        vistas.update(vistas=0)
        visitas=Post.objects.all()
        visitas.update(visitas=0)

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


    context={"date": date, "post": post, 'primer_post': primer_post, 'post_all': post_all, 'form': form, 'total': total, 'categoria': categoria}

    return render(request, 'home.html', context)

@login_required
def porfile(request):
    user=request.user
    porfile=get_object_or_404(Porfile, pk=user.porfile.pk)
    posts=Post.objects.all().filter(autor=user.porfile).order_by('-id_post')
    post_count=posts.count()
    categoria=Post.objects.all().order_by('-visitas')[:10]
    context={ 'categoria': categoria, 'porfile': porfile, 'user': user, 'posts': posts, 'post_count': post_count}
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

    categoria=Post.objects.all().order_by('-visitas')[:10]
    post=Post.objects.all().order_by('-visitas')[:100]



    context={'categoria': categoria, 'form': form,'post': post }
    return render(request, 'top.html', context)

@login_required
def post_details(request, pk):

    actual_user=request.user
    post_details = get_object_or_404(Post, pk=pk)
    post_guardado = get_object_or_None(PostGuardado, post=pk, usuario=request.user)
    guardado=False
    if post_guardado!=None:
        guardado=True


    porfile=Porfile.objects.get(usuario=request.user)
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



    categoria=Post.objects.all().order_by('-visitas')[:10]
    post_details.visitas=post_details.visitas+1
    post_details.save()
    porfile=get_object_or_404(Porfile, usuario=post_details.autor.usuario  )
    context={'post_details': post_details, 'porfile': porfile, 'form': form, 'categoria': categoria, 'comment_form': comment_form, 'comentarios': comentarios, 'comentario': comentario,'actual_user': actual_user, 'guardado': guardado}
    return render(request, 'post_details.html', context)


def guardar_post(request, pk):
    user=request.user
    post = get_object_or_404(Post, pk=pk)
    guardar=PostGuardado.objects.create(usuario=user, post=post)
    guardar.save()
    return redirect('post_guardados');

def post_guardados(request):
    user=request.user
    post_guardados=PostGuardado.objects.all().filter(usuario=user).order_by('-id_post_guardado')
    return render(request, 'post_guardados.html',{'post': post_guardados})

def guardado_quit(request, pk):
    user=request.user
    borrar_post_guardado=get_object_or_404(PostGuardado, post=pk, usuario=user).delete()
    return redirect("post_guardados")


def categoria(request, slug):
    categoria=Post.objects.all().order_by('-visitas')[:10]
    cat=Post.objects.all().order_by('-visitas').filter(categoria=slug)[:50]



    context={'categoria': categoria, 'cat': cat}
    return render(request, 'categoria_details.html', context)


def register(request):
    categoria=Post.objects.all().order_by('-visitas')[:10]
    # Creamos el formulario de autenticación vacío
    form_reg = UserCreationForm()
    x = form_reg.fields['username']
    x.help_text = "Escoge un nombre de usuario"

    y = form_reg.fields['password1']
    y.help_text = "Escribe una contraseña"

    z = form_reg.fields['password2']
    z.help_text = "Confirma tu contraseña"
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form_reg = UserCreationForm(data=request.POST)

        # Si el formulario es válido...
        if form_reg.is_valid():
            # Creamos la nueva cuenta de usuario
            user = form_reg.save()

            # Si el usuario se crea correctamente
            if user is not None:
                # Hacemos el login manualmente
                do_login(request, user)
                # Y le redireccionamos a la portada
                return redirect('/')

    # Si llegamos al final renderizamos el formulario
    return render(request, "register.html", {'form_reg': form_reg, 'categoria': categoria})


def login(request):
    categoria=Post.objects.all().order_by('-visitas')[:10]
    # Creamos el formulario de autenticación vacío
    form_auth = AuthenticationForm()
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form_auth = AuthenticationForm(data=request.POST)
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
                do_login(request, user)
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
            articulo= Post.objects.create(titulo=titulo,    descripcion=descripcion ,articulo=articulo,categoria=categoria, autor=autor, imagen_principal=imagen_principal  )
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
    user=get_object_or_404(Porfile, id_porfile=pk)



    posts=Post.objects.all().filter(autor=user).order_by('-id_post')
    post_count=posts.count()
    return render(request, 'view_porfile.html',{'user': user, 'posts': posts,'post_count': post_count})
