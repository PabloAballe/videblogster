from django.urls import path, include
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('top', views.top, name='top'),
    path('privacy', views.privacy, name='privacy'),
    path('view_porfile/<int:pk>/', views.view_porfile, name='view_porfile'),
    path('guardar_post/<int:pk>/', views.guardar_post, name='guardar_post'),
    path('faq', views.faq, name='faq'),
    path('categoria/<slug:slug>/', views.categoria, name='categoria'),
    path('404', views.no_existe, name='no_existe'),
    path('porfile', views.porfile, name='porfile'),
    path('post_guardados', views.post_guardados, name='post_guardados'),
    path('post/borrar/guardado/<int:pk>/', views.guardado_quit, name='guardado_quit'),
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
]
