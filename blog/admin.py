from django.contrib import admin
from .models import Post
from .models import Porfile
from .models import Comentario
from .models import PostGuardado
from django_summernote.admin import SummernoteModelAdmin

class PostAdmin1(SummernoteModelAdmin):
    summernote_fields = ('articulo',)

class PostAdmin(admin.ModelAdmin):
    list_display= ['titulo', 'categoria', 'created_at']
    search_fields = ['titulo', 'articulo', 'categoria', 'created_at']
    list_filter =  ['titulo',  'categoria', 'created_at']

class PorfileAdmin(admin.ModelAdmin):
    list_display=[ 'id_porfile','email','vistas']
    search_fields = [ 'email','vistas']
    list_filter =['email','vistas']

class ComentarioAdmin(admin.ModelAdmin):
    list_display= ['created_at']
    search_fields = ['publicado', 'created_at']
    list_filter = ['publicado', 'created_at']

class PostGuardadoAdmin(admin.ModelAdmin):
    list_display= ['id_post_guardado','guardado_el']
    search_fields = ['id_post_guardado','guardado_el']
    list_filter = ['id_post_guardado','guardado_el']


admin.site.site_header = "Blogster"
admin.site.site_title = "Blogster | Portal"
admin.site.index_title = "Blogster | Portal"


admin.site.register(Post, PostAdmin)
admin.site.register(Porfile, PorfileAdmin)
admin.site.register(Comentario, ComentarioAdmin)
admin.site.register(PostGuardado, PostGuardadoAdmin)
