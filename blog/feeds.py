from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import Categorias

class RandomPost(Feed):
    title = "Feed VideoBlogster"
    link = "feed/randompost"
    description  = "Feed from videos in VideoBlogster"

    def item(self):
       return Categorias.objects.all()


    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    # item_link is only needed if NewsItem has no get_absolute_url method.
    # def item_link(self, item):
    #     return reverse('news-item', args=[item.pk])