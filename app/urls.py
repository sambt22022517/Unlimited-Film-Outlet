from django.urls import path, re_path
from django.conf.urls.static import static
from django.conf import settings
from .views import home, user, index, filter, film, cart, bill
from django.views.static import serve

urlpatterns = [
    path('', home.home, name='home'),
    path('home/', home.home, name='home'),
    
    path('index/', index.index, name='index'),

    path('login/', user.login, name='login'),
    path('logout/', user.logout, name='logout'),
    path('register/', user.register, name='register'),
    path('profile/', user.profile, name='profile'),
    path('profile/edit/', user.edit_profile, name='edit_profile'),

    path('search/', filter.search, name='search'),
    path('recommend/', filter.recommend, name='recommend'),

    path('film/<str:film_id>/', film.film_detail, name='film_detail'),

    path('cart/', cart.render_get_cart, name='render_get_cart'),
    path('add-to-cart/', cart.render_add_cart, name='render_add_cart'),
    path('cart/remove/<str:item_id>/', cart.remove_from_cart, name='remove_from_cart'),
    path('cart/select/<str:item_id>/', cart.select_cart_item, name='select_cart_item'),

    path('confirm-payment/<str:type>/', bill.render_bill_for_payment, name='render_bill_for_payment'),
    path('bill/<int:bill_id>/', bill.render_bill, name='render_bill'),
    path('all-bill/', bill.render_all_bill, name='render_all_bill'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, }), ]