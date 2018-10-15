from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as _UserAdmin

from .models import Article, Category, Tag, User


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time', 'modified_time', 'category', 'author']


class UserAdmin(_UserAdmin):
    def __init__(self, *args, **kwargs):
        super(UserAdmin, self).__init__(*args, **kwargs)
        self.list_display = self.list_display + ('nickname',)
        self.list_filter = self.list_display + ('nickname',)

admin.site.register(Article, ArticleAdmin)
admin.site.register(Category)
admin.site.register(User, UserAdmin)
