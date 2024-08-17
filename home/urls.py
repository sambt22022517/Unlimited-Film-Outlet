from django.urls import path
from . import views

urlpatterns = [
    path('home', views.render_home, name='Home'),
]