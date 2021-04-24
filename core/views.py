from django.views import generic
from .models import NewsItem

class NewsItemListview(generic.ListView):
    model = NewsItem
    template_name = 'news_item_list.html'