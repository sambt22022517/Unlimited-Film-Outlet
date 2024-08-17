from django.shortcuts import render, redirect
from .models import *
from .cart import *

# Create your views here.

#login_require
def render_add_cart(request):
    if request.method == 'POST':
        try:
            id_user = request.session['id_user']
            user = User.objects.get(id = id_user)
            id_film = request.POST['id_film']
            film = Film.objects.get(id = id_film)

            status, notification = add_cart(film, user)

            return render(request, 'viewdetailfilm.html', {
                'status': status, 
                'notification': notification,
                'film': film})
        except:
            return redirect('Home')
    return redirect('Viewallfilm')

#login_require
def render_update_cart(request):
    if request.method == 'POST':
        id_cart = request.POST['id_cart']
        action = request.POST['action']
        if not id_cart or not action:
            return redirect('Viewcart')

        cart = Cart.objects.get(id = id_cart)
        status, notification = update_cart(cart, action)

        return redirect('Viewcart')
    
    return redirect('Viewcart')

#login_require
def render_get_cart(request):
    if 'id_user' not in request.session:
        return redirect('Home')
        
    # Lấy id người dùng từ session
    id_user = request.session['id_user']
    
    # Lấy người dùng từ cơ sở dữ liệu
    user = User.objects.get(id=id_user)
    
    # Lấy giỏ hàng của người dùng
    carts = Cart.objects.filter(user=user)
    
    # Render trang giỏ hàng với dữ liệu
    return render(request, 'viewcart.html', {'carts': carts})