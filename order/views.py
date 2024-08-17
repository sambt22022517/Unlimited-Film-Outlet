from django.shortcuts import render, redirect
from .order import *
import paypalrestsdk
from paypalrestsdk import Payment

# Create your views here.
def render_bill_for_payment(request):
    # render ra bill để người dùng xem và thanh toán
    id_user = request.session.get('id_user')
    if not id_user:
        return redirect('login')  # Nếu không có id_user trong session, yêu cầu đăng nhập
    user = User.objects.get(id=id_user)
    carts = Cart.objects.filter(user=user, selected=True)

    if not carts.exists():
        return redirect('cart')  # Nếu giỏ hàng trống, chuyển hướng đến trang giỏ hàng

    total_price = Decimal(0)
    films = []

    for cart in carts:
        film = cart.film
        price = film.price
        total_price += price
        films.append(film)

    return render(request, 'viewbillforpayment.html', {'films': films, 'total_price': total_price})

def render_pay_success(request):
    create_bill(request, COMPLETE)
    return render(request, 'success.html')

def render_pay_fail(request):
    create_bill(request, CANCELLED)
    return render(request, 'fail.html')

def render_pay_error(request):
    create_bill(request, ERROR)
    return render(request, 'error.html')

def render_payment(request):
    if request.method == "POST":
        try:
            print("Call Paypal Payment")

            id_user = request.session.get('id_user')
            if not id_user:
                return redirect('login')  # Nếu không có id_user trong session, yêu cầu đăng nhập

            user = User.objects.get(id=id_user)
            carts = Cart.objects.filter(user=user, selected=True)

            if not carts.exists():
                return redirect('cart')  # Nếu giỏ hàng trống, chuyển hướng đến trang giỏ hàng

            total_price = Decimal(0)
            films = []

            for cart in carts:
                film = cart.film
                price = film.price
                total_price += price
                films.append(film)

            payment = Payment({
                "intent": "sale",
                "payer": {
                    "payment_method": "paypal"},
                "redirect_urls": {
                    "return_url": "http://localhost:8000/paysuccess",
                    "cancel_url": "http://localhost:8000/payfail"},
                "transactions": [{
                    "item_list": {
                        "items": [{
                            "name": film.film_name,
                            "price": str(film.price),
                            "currency": "USD",
                            "quantity": 1,
                            } for film in films]},
                    "amount": {
                        "total": str(total_price),
                        "currency": "USD"},
                    "description": "This is the payment description."}]
            })

            if payment.create():
                print("Payment created successfully")
                for link in payment.links:
                    if link.rel == "approval_url":
                        approval_url = str(link.href)
                        return redirect(approval_url)
            else:
                print(payment.error)
                return redirect('Payfail')  # Thêm trang thất bại thanh toán

        except Exception as e:
            print(f"Error: {e}")
            return redirect('Payerror')  # Thêm trang lỗi chung

    return redirect('Viewbillforpayment')

def render_bill(request):
    id_user = request.session.get('id_user')
    if not id_user:
        return redirect('login')  # Nếu không có id_user trong session, yêu cầu đăng nhập
    if request.method == 'POST':
        id_bill = request.POST['id_bill']
        bill = Bill.objects.get(id = id_bill)

        bill_items = BillItem.objects.filter(bill = bill)
        return render(request, 'viewbill.html', {'bill': bill, 'bill_items': bill_items})

    return redirect("Viewallbill") 
def render_all_bill(request):
    id_user = request.session.get('id_user')
    if not id_user:
        return redirect('login')  # Nếu không có id_user trong session, yêu cầu đăng nhập
    
    # lấy bill
    user = User.objects.get(id = id_user)
    bills = Bill.objects.filter(user = user)

    return render(request, 'viewallbill.html', {'bills': bills})