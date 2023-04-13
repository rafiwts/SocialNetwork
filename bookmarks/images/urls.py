from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path(r'create/', views.image_create, name='create'),
    path(r'detail/<int:id>/<slug:slug>', views.image_detail, name='detail'),
    path(r'like/', views.image_like, name="like"),
    path(r'', views.image_list, name='list')
]