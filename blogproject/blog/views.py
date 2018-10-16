from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, FormView

from blog.forms import CommentForm
from blog.models import Article


class IndexView(ListView):
    model = Article
    template_name = 'blog/index.html'
    context_object_name = 'article_list'
    paginate_by = settings.PER_PAGE


class PostDetailView(DetailView):
    model = Article
    template_name = 'blog/detail.html'
    context_object_name = 'article'

    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response


class CommentView(FormView):
    form_class = CommentForm
    success_url = reverse_lazy('users:success')
    template_name = 'users/base_form.html'
    title = 'Password change'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        article = self.get_article()
        setattr(self, 'title', f'{article.title}-留言')
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super(CommentView, self).get_context_data(**kwargs)
        article = self.get_article()
        context_data.update({'title': f'{article.title}-留言'})
        return context_data

    def get_article(self):
        try:
            article = self.article
        except AttributeError:
            pk = self.kwargs.get('pk')
            article = get_object_or_404(Article, pk=pk)
            setattr(self, 'article', article)
        return article

    def form_valid(self, form):
        form = self.get_form()
        form.instance.user = self.request.user
        form.instance.article = self.get_article()
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:detail', kwargs={'pk': self.kwargs.get('pk')})


class SearchView(IndexView):
    def get_queryset(self):
        q = self.request.GET.get('q', '')
        return super(SearchView, self).get_queryset().filter(
            Q(title__icontains=q) | Q(content__icontains=q) | Q(excerpt__icontains=q))


class ArchiveView(IndexView):
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchiveView, self).get_queryset().filter(
            created_time__year=year, created_time__month=month
        )


class CategoryView(IndexView):
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return super(CategoryView, self).get_queryset().filter(category__pk=pk)


class TagView(IndexView):
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return super(TagView, self).get_queryset().filter(tags__pk=pk)
