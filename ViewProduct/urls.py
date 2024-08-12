from django.urls import path
from . import views

urlpatterns = [
    path('view-detail/<int:movie_id>', views.ViewDetail, name='ViewDetail'),
    path('view-product', views.ViewProduct, name='ViewProduct'),
    path('Cart', views.Cart, name='Cart')
]
