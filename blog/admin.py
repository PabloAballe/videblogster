from django.contrib import admin
from .models import Post
from .models import Porfile
from .models import Comentario
from .models import PostGuardado
from django_summernote.admin import SummernoteModelAdmin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import *


class PostAdmin1(SummernoteModelAdmin):
    summernote_fields = ('articulo',)

class CondicionesAdmin(SummernoteModelAdmin):
    summernote_fields = '__all__'

class PostAdmin(SummernoteModelAdmin):
    summernote_fields = '__all__'
    list_display= ['titulo', 'categoria', 'created_at']
    search_fields = ['titulo', 'articulo', 'categoria', 'created_at']
    list_filter =  ['titulo',  'categoria', 'created_at']


class PorfileAdmin(ImportExportModelAdmin):
    list_display=[ 'id_porfile','paypal','vistas']
    search_fields = [ 'id_porfile','paypal','vistas']
    list_filter =['paypal','vistas']


class ComentarioAdmin(admin.ModelAdmin):
    list_display= ['created_at']
    search_fields = ['publicado', 'created_at']
    list_filter = ['publicado', 'created_at']

class PostGuardadoAdmin(admin.ModelAdmin):
    list_display= ['id_post_guardado','guardado_el']
    search_fields = ['id_post_guardado','guardado_el']
    list_filter = ['id_post_guardado','guardado_el']


class SeguidoresAdmin(admin.ModelAdmin):
    list_display= ['sigue','seguido', 'seguiendo_desde']
    search_fields = ['sigue','seguido', 'seguiendo_desde']
    list_filter = ['sigue','seguido', 'seguiendo_desde']

class CategoriasAdmin(admin.ModelAdmin):
    list_display= ['categoria_nombre','creada_el']
    search_fields = ['categoria_nombre','creada_el']
    list_filter = ['categoria_nombre','creada_el']

admin.site.site_header = "Blogster"
admin.site.site_title = "Blogster | Portal"
admin.site.index_title = "Blogster | Portal"


admin.site.register(Post, PostAdmin)
admin.site.register(Porfile, PorfileAdmin)
admin.site.register(Comentario, ComentarioAdmin)
admin.site.register(PostGuardado, PostGuardadoAdmin)
admin.site.register(Seguidores, SeguidoresAdmin)
admin.site.register(Categorias, CategoriasAdmin)
admin.site.register(Condicion, CondicionesAdmin)
