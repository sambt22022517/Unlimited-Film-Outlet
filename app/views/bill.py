from ..models import User, Cart, BillItem, Bill, Film
from django.shortcuts import render, redirect
from ..serializers import FilmSerializer
from datetime import datetime
from django.http import JsonResponse
import json

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

    if request.method == 'POST':
        if type == 'create':
            data = json.loads(request.body)
            total_price = data.get('total_price')

            carts = Cart.objects.filter(user=user, selected=True)
            bill = Bill(user=user, payment_date=datetime.now(), total_price=total_price)
            bill.save()
            for cart in carts:
                item = BillItem(bill=bill, film=cart.film)
                item.save()
                cart.delete()
            return JsonResponse({'success': True, 'type': bill.id,}, status=200)
        elif type == 'buynow':
            data = json.loads(request.body)
            total_price = data.get('total_price')
            film_id = data.get('film_id')
            
            bill = Bill(user=user, payment_date=datetime.now(), total_price=total_price)
            bill.save()
            
            film = Film.objects.get(id=film_id)
            item = BillItem(bill=bill, film=film)
            item.save()
            return JsonResponse({'success': True, 'type': bill.id,}, status=200)

    bill = Bill.objects.get(id=int(type))
    items = BillItem.objects.filter(bill=bill)
    films = []
    for item in items:
        films.append(item.film)
    serializer = FilmSerializer(films, many=True, context={'request': request})

    response_data.update({
        'films': serializer.data,
        'total_price': bill.total_price,
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

        if action == 'checkout':
            bill.status = COMPLETE
            bill.save()
        elif action == 'cancel':
            bill.status = CANCELLED
            bill.save()
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
    bills = Bill.objects.filter(user=user).order_by('-payment_date')
    response_data = {
        'user_name': user.user_name,
        'email': user.email,
        'num_items_in_cart': num_items_in_cart,
        'user_logged_in': True,
        'bills': bills,
    }

    return render(request, 'bill/all_bill.html', response_data)