from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CASCADE


class User(AbstractUser):
    nickname = models.CharField(max_length=32, verbose_name='昵称')

    class Meta(AbstractUser.Meta):
        pass


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='名称')

    class Meta:
        verbose_name = '类别'
        verbose_name_plural = verbose_name


class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name='名称')

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
        verbose_name = '标签'
        verbose_name_plural = verbose_name
