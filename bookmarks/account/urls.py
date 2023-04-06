from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    # path('login/', views.user_login, name='login'),
    path('', include('django.contrib.auth.urls')) # for methods like login, logout, logout_then_login etc - it looks for registration folder (with html files), see notes
]
