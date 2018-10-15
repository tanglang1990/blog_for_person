from django.urls import path, include

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<pk>', views.detail, name='detail'),
]
