from django.urls import path
from . import views

urlpatterns = [
    path('addcart', views.render_add_cart, name='Addcart'),
    path('updatecart', views.render_update_cart, name='Updatecart'),
    path('viewcart', views.render_get_cart, name='Viewcart'),
]