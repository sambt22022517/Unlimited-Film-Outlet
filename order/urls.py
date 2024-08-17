from django.urls import path
from . import views

urlpatterns = [
    path('viewbillforpayment/', views.render_bill_for_payment, name='Viewbillforpayment'),
    path('paysuccess/', views.render_pay_success, name='Paysuccess'),
    path('payfail/', views.render_pay_fail, name='Payfail'),
    path('payerror/', views.render_pay_fail, name='Payerror'),
    path('payment/', views.render_payment, name='Payment'),
    path('viewbill/', views.render_bill, name='Viewbill'),
    path('viewallbill/', views.render_all_bill, name='Viewallbill'),
]