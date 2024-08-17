from django.urls import path
from . import views

urlpatterns = [
    path('viewallfilm/', views.render_all_film, name='Viewallfilm'),
    path('viewdetailfilm/<int:id_film>/', views.render_film, name='Viewdetailfilm'),
]