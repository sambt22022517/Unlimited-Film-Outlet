from .models import *
from .models import *
from decimal import Decimal
from django.utils import timezone

COMPLETE = 'P'
ERROR = 'E'
CANCELLED = 'C'

def create_bill(request, status):
    id_user = request.session.get('id_user')
    if not id_user:
        return False  # Nếu không có id_user trong session, không thể tạo bill

    user = User.objects.get(id=id_user)
    carts = Cart.objects.filter(user=user, selected=True)

    if not carts.exists():
        return False  # Nếu giỏ hàng trống, không thể tạo bill

    total_price = Decimal(0)
    films = []

    for cart in carts:
        film = cart.film
        price = film.price
        total_price += price
        films.append(film)
    
    # Tạo bill
    bill = Bill.objects.create(
        user=user,
        payment_date=timezone.now(),
        total_price=total_price,
        status = status
    )

    for film in films:
        BillItem.objects.create(
            bill=bill,
            film=film,
        )
    carts.delete()
    return True
