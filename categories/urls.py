from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('create-category', views.create_category, name='create_category'),
    path('list', views.category_list, name='list'),
]