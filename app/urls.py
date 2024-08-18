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
    path('film/<str:film_id>/', views.film_detail, name='film_detail'),
    path('recommend/', views.recommend, name='recommend'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('addcart/', views.render_add_cart, name='Addcart'),
    path('updatecart/', views.render_update_cart, name='Updatecart'),
    path('viewcart/', views.render_get_cart, name='Viewcart'),
    path('viewbillforpayment/', views.render_bill_for_payment, name='Viewbillforpayment'),
    path('paysuccess/', views.render_pay_success, name='Paysuccess'),
    path('payfail/', views.render_pay_fail, name='Payfail'),
    path('payerror/', views.render_pay_fail, name='Payerror'),
    path('payment/', views.render_payment, name='Payment'),
    path('viewbill/', views.render_bill, name='Viewbill'),
    path('viewallbill/', views.render_all_bill, name='Viewallbill'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)