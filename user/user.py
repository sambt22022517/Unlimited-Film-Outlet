from .models import *
from cart.models import Cart


def login(user_name, password):

    # kiểm tra người dùng nhập đủ thông tin
    # kiểm tra người dùng nhập đúng tên đăng nhập, nếu đúng, kiểm tra tiếp người dùng nhập đúng mật khẩu

    if "" in [user_name, password]:
        return ('False', "Chưa nhập đủ thông tin")
    elif User.objects.filter(user_name = user_name):
        user = User.objects.get(user_name = user_name)
        if user.password == password:
            return ('True',None)
        else:
            return ('False', "Tên đăng nhập hoặc mật khẩu bị sai")
    else:
        return ('False', "Tên đăng nhập hoặc mật khẩu bị sai")
    
def logout():
    pass

def register(user_name, password, repeat_password, email):
    # chưa nhập đủ thông tin
    # tên đăng nhập, email trùng lặp
    # mật khẩu không khớp

    if "" in [user_name, password, repeat_password, email]:
        return ('False', "Chưa nhập đủ thông tin")
    elif User.objects.filter(user_name = user_name) or User.objects.filter(email = email):
        return ('False', "Tên đăng nhập hoặc email đã tồn tại")
    elif password != repeat_password:
        return ('False', "Mật khẩu không khớp")
    else:
        #lưu lại các thông tin đăng kí
        # cart = Cart.objects.create()
        user = User.objects.create(
            user_name = user_name,
            email = email,
            password = password
        )
        
        return ('True', "Đăng kí thành công")
        
def info():
    pass