from django.urls import path
from . import views

urlpatterns = [
    path('login', views.render_login, name='Login'),
    path('register', views.render_register, name='Register'),
    path('logout', views.render_logout, name='Logout'),
]