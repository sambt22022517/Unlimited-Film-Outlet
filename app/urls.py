from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('index/', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path('search/', views.search, name='search'),
    path('film/<int:film_id>/', views.film_detail, name='film_detail'),
    path('recommend/', views.recommend, name='recommend'),
]