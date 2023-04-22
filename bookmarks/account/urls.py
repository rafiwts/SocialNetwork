from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    # path('login/', views.user_login, name='login'),
    path('', include('django.contrib.auth.urls')), # for methods like login, logout, logout_then_login etc - it looks for registration folder (with html files), see notes
    path('myblog/', views.my_blog, name='my_blog'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit_profile, name='edit'),
    path('users/', views.user_list, name='user_list'),
    path('users/follow/', views.user_follow, name='user_follow'),
    path('users/<username>/', views.user_detail, name='user_detail'),   
]
