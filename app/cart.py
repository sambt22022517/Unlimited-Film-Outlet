from .models import *
from django.shortcuts import get_object_or_404

def add_cart(film, user):
    # Kiểm tra xem phim đã có trong giỏ hàng của người dùng chưa
    if Cart.objects.filter(user=user, film=film).exists():
        return (False, "Đã có phim này trong giỏ hàng")
    else:
        # Tạo một bản ghi mới cho phim trong giỏ hàng của người dùng
        Cart.objects.create(
            user=user,
            film=film,
            selected=False  # Thiết lập giá trị mặc định cho selected
        )
        return (True, "Thêm vào giỏ hàng thành công")

def update_cart(cart, prompt):
    # xóa phim
    # chuyển trạng thái selected
    if prompt == "DELETE":
        cart.delete()
        return (True, "Xóa thành công")
    elif prompt == "TRANSFORM SELECTED":
        selected = cart.selected
        cart.selected = not selected
        cart.save()
        return ("True", "Chuyển thành công")
    else:
        return (False, "Không thể thực hiện hành vi")

def get_cart():
    pass