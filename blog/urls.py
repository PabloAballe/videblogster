from django.conf.urls import  url, include
from . import views
from django.contrib.sitemaps.views import sitemap
from .sitemaps import PostSitemap
from django.views.generic.base import TemplateView
from .models import Post
from django.conf.urls import url
from django.contrib.auth import views as auth_views

from django.urls import path

sitemaps = {
    'posts': PostSitemap,
}




urlpatterns = [
    path('', views.home, name='home'),
    path('ads.txt', views.ads_txt, name='ads.txt'),
    path('top', views.top, name='top'),
    path('api_download', views.api_download, name='api_download'),
    path('siguiendo/<int:pk>/', views.siguiendo, name='siguiendo'),
    path('seguidores/<int:pk>/', views.seguidores, name='seguidores'),
    path('seguir/<int:pk>/', views.seguir, name='seguir'),
    path('dejar_seguir/<int:pk>/', views.dejar_seguir, name='dejar_seguir'),
    path('privacy', views.privacy, name='privacy'),
    path('view_porfile/<int:pk>/', views.view_porfile, name='view_porfile'),
    path('guardar_post/<int:pk>/', views.guardar_post, name='guardar_post'),
    path('faq', views.faq, name='faq'),
    path('categoria/<int:pk>/', views.categoria, name='categoria'),
    path('404', views.no_existe, name='no_existe'),
    path('porfile', views.porfile, name='porfile'),
    path('post_guardados', views.post_guardados, name='post_guardados'),
    path('post/quitar/guardado/<int:pk>/', views.guardado_quit, name='guardado_quit'),
    path('liked_post', views.liked_post, name='liked_post'),
    path('post/borrar/like/<int:pk>/', views.like_quit, name='like_quit'),
    path('edit/porfile', views.update_profile, name='edit_porfile'),
    path('post/<int:pk>/', views.post_details, name='post_details'),
    path('summernote/', include('django_summernote.urls')),
    path('register', views.register,name="register"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('post/new/', views.post_new, name='post_new'),
    path('delete/<int:pk>/', views.delete, name='delete'),
    path('delete_post/<int:pk>/', views.delete_post, name='delete_post'),
    path('post/edit/<int:pk>/', views.post_edit, name='post_edit'),
    path('comment/delete/<int:pk>/', views.delete_com, name='delete_com'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt',TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),),
    path('accounts/reset_password/', auth_views.PasswordResetView.as_view(), name ='password_reset'),
    path('accounts/reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name ='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name ='password_reset_confirm'),
    path('accounts/reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name ='password_reset_complete'),
]
