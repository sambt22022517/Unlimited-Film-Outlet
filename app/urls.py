from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
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
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)