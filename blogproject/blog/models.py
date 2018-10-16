import markdown
from django.urls import reverse

from users.models import User
from django.db import models
from django.db.models import CASCADE
from django.utils.html import strip_tags


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='名称')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '类别'
        verbose_name_plural = verbose_name


class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name='名称')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name


class Article(models.Model):
    title = models.CharField(max_length=70, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    modified_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    excerpt = models.CharField(max_length=200, blank=True, verbose_name='摘录')
    category = models.ForeignKey(Category, on_delete=CASCADE, verbose_name='类别')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='标签')
    views = models.PositiveIntegerField(default=0, verbose_name='浏览次数')
    author = models.ForeignKey(User, on_delete=CASCADE, verbose_name='作者')

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):
        if not self.excerpt:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            self.excerpt = strip_tags(md.convert(self.content))[:54]
        super(Article, self).save(*args, **kwargs)

    def md_content(self):
        return markdown.markdown(
            self.content,
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
            ])


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, verbose_name='用户')
    article = models.ForeignKey('Article', on_delete=CASCADE, verbose_name='文章')
    content = models.TextField(verbose_name='内容')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content
