from django.urls import path, include

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<pk>', views.detail, name='detail'),
    path('comment/<pk>', views.comment, name='comment'),
    path('search/', views.search, name='search'),
    path('archive/<year>/<month>/', views.archive, name='archive'),
    path('category/<pk>/', views.category, name='category'),
    path('tag/<pk>/', views.tag, name='tag'),
]
