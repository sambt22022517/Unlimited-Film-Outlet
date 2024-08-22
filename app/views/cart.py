from django.shortcuts import render, redirect
import json
from ..models import User, Film, Cart
from django.http import JsonResponse
from ..serializers import CartSerializer

def add_cart(film, user, selected):
    num_items_in_cart = len(Cart.objects.filter(user=user))

    if Cart.objects.filter(user=user, film=film).exists():
        return (num_items_in_cart, "Đã có phim này trong giỏ hàng")
    
    Cart.objects.create(
        user=user,
        film=film,
        selected=bool(selected)
    )
    return (num_items_in_cart+1, "Thêm vào giỏ hàng thành công")

def render_add_cart(request):
    user_id = request.session['user_id']
    if not user_id:
        return redirect('login')
    
    if request.method == 'POST':
        data = json.loads(request.body)
        id_film = data.get('film_id')
        selected = data.get('selected')

        user = User.objects.get(id=user_id)
        film = Film.objects.get(id=id_film)

        num_items_in_cart, notification = add_cart(film, user, selected)
        return JsonResponse({
            'success': True,
            'num_items_in_cart': num_items_in_cart,
        })
    return JsonResponse({'success': False}, status=400)

def render_get_cart(request):
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
    
    # Lấy thông tin giỏ hàng
    user = User.objects.get(id=user_id)
    carts = Cart.objects.filter(user=user)
    serializer = CartSerializer(carts, many=True, context={'request': request})

    response_data.update({
        'carts': serializer.data,
    })
    
    # Render trang giỏ hàng với dữ liệu
    return render(request, 'cart/cart.html', response_data)

def remove_from_cart(request, item_id):
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

    if request.method == 'DELETE':
        item = Cart.objects.get(id=item_id)
        item.delete()
        response_data.update({'success': True})
        response_data.update({'num_items_in_cart': num_items_in_cart-1})
        return JsonResponse(response_data, status=200)
    
    response_data.update({'success': False})
    return JsonResponse(response_data, status=404)

def select_cart_item(request, item_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        selected = data.get('selected')
        
        item = Cart.objects.get(id=item_id)
        item.selected = selected
        item.save()
        return JsonResponse({'success': True}, status=200)
    return JsonResponse({'success': False, 'error': "Method phải là POST"}, status=404)