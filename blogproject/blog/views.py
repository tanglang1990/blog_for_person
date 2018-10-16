from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from blog.forms import CommentForm
from blog.models import Article


def index(request):
    page = request.GET.get('page')
    article_list = Article.objects.all()
    paginator = Paginator(article_list, settings.PER_PAGE)
    article_list = paginator.get_page(page)
    context = {'article_list': article_list, 'title': settings.TITLE}
    return render(request, 'blog/index.html', context=context)


def detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.increase_views()
    return render(request, 'blog/detail.html', context={'article': article})


@login_required
def comment(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            form.instance.article = article
            form.instance.user = request.user
            form.save()
            return redirect(article)
    else:
        form = CommentForm()
    return render(
        request, 'users/base_form.html', {'title': f'{article.title}-留言', 'form': form})


def search(request):
    q = request.GET.get('q')
    article_list = Article.objects.filter(
        Q(title__icontains=q) | Q(content__icontains=q) | Q(excerpt__icontains=q))
    return render(request, 'blog/index.html', {'article_list': article_list})


def archive(request, year, month):
    article_list = Article.objects.filter(
        created_time__year=year, created_time__month=month
    )
    return render(request, 'blog/index.html', context={'article_list': article_list})


def category(request, pk):
    article_list = Article.objects.filter(category__pk=pk)
    return render(request, 'blog/index.html', context={'article_list': article_list})


def tag(request, pk):
    article_list = Article.objects.filter(tags__pk=pk)
    return render(request, 'blog/index.html', context={'article_list': article_list})
