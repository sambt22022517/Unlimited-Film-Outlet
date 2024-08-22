from ..models import User, Cart, BillItem, Bill
from django.shortcuts import render, redirect
from ..serializers import FilmSerializer
from datetime import datetime
from django.http import JsonResponse

COMPLETE = 'P'
ERROR = 'E'
CANCELLED = 'C'

def render_bill_for_payment(request, type):
    user_id = request.session.get('user_id')

    if user_id:
        user = User.objects.get(id=user_id)
    else:
        return redirect('login')
    
    num_items_in_cart = len(Cart.objects.filter(user=user))
    response_data = {
        'user_name': user.user_name,
        'email': user.email,
        'num_items_in_cart': num_items_in_cart,
        'user_logged_in': True,
    }
    
    carts = Cart.objects.filter(user=user, selected=True)
    film_price = 0
    films = []
    for cart in carts:
        film = cart.film
        price = film.price
        film_price += price
        films.append(film)
    serializer = FilmSerializer(films, many=True, context={'request': request})

    if request.method == 'POST':
        bill = Bill(user=user, payment_date=datetime.now(), total_price=film_price)
        bill.save()
        for cart in carts:
            billitem = BillItem(bill=bill, film=cart.film)
            billitem.save()
        return JsonResponse({'success': True, 'type': bill.id,}, status=200)
    else:
        bill = Bill.objects.get(id=int(type))

    response_data.update({
        'films': serializer.data,
        'total_price': film_price,
        'bill': bill,
    })

    return render(request, 'bill/confirm_payment.html', response_data)

def render_bill(request, bill_id):
    user_id = request.session.get('user_id')

    if user_id:
        user = User.objects.get(id=user_id)
    else:
        return redirect('login')
    
    response_data = {
        'user_name': user.user_name,
        'email': user.email,
        'user_logged_in': True,
    }
    
    bill = Bill.objects.get(id=bill_id)
    if request.method == 'POST':
        action = request.POST.get('action')

        carts = Cart.objects.filter(user=user, selected=True)

        if action == 'checkout':
            bill.status = COMPLETE
            bill.save()
            carts.delete()
        elif action == 'cancel':
            bill.status = CANCELLED
            bill.save()
            carts.delete()
        elif action == 'back':
            return redirect('/cart')
        elif action == 'list-bill':
            return redirect('/all-bill')
        
    billItem = BillItem.objects.filter(bill=bill)
    films = []
    for item in billItem:
        film = item.film
        films.append(film)
    serializer = FilmSerializer(films, many=True, context={'request': request})
    num_items_in_cart = len(Cart.objects.filter(user=user))

    response_data.update({
        'bill': bill,
        'films': serializer.data,
        'num_items_in_cart': num_items_in_cart,
    })
    
    return render(request, 'bill/bill.html', response_data)

def render_all_bill(request):
    user_id = request.session.get('user_id')

    if user_id:
        user = User.objects.get(id=user_id)
    else:
        return redirect('login')
    
    num_items_in_cart = len(Cart.objects.filter(user=user))
    bills = Bill.objects.filter(user=user)
    response_data = {
        'user_name': user.user_name,
        'email': user.email,
        'num_items_in_cart': num_items_in_cart,
        'user_logged_in': True,
        'bills': bills,
    }

    return render(request, 'bill/all_bill.html', response_data)