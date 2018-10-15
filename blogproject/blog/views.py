from django.conf import settings
from django.shortcuts import render, get_object_or_404

from blog.models import Article


def index(request):
    article_list = Article.objects.all().order_by('-created_time')
    return render(request, 'blog/index.html', context={'article_list': article_list, 'title': settings.TITLE})


def detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'blog/detail.html', context={'article': article})
