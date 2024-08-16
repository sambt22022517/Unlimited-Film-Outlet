from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Film, Habit
from .ml_model import RecommendModel
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Case, When
from django import forms
import numpy as np
import random

recommend_model = RecommendModel()
genres = {
    "Chính kịch": 0,
    "Âm nhạc": 1,
    "Nhạc kịch": 2,
    "Giả tưởng": 3,
    "Hành động": 4,
    "Phiêu lưu": 5,
    "Hài kịch": 6,
    "Bí ẩn": 7,
    "Khoa học viễn tưởng": 8,
    "Phim ngắn": 9,
    "Kinh dị tâm lý": 10,
    "Kinh dị": 11,
    "Tiểu sử": 12,
    "Thể thao": 13,
    "Lãng mạn": 14,
    "Gia đình": 15,
    "Lịch sử": 16,
    "Hoạt hình": 17,
    "Tài liệu": 18,
    "Hình sự": 19,
    "Chiến tranh": 20,
    "Miền Tây hoang dã": 21,
    "Trực tiếp": 22,
    "Trò chơi truyền hình": 23,
    "Thoại mục": 24,
    "Tin tức": 25,
    "Phim người lớn": 26,
}

def index(request):
    if not request.session.get('user_id'):
        return redirect('login')
    return render(request=request, template_name='index.html')

def home(request):
    user_id = request.session.get('user_id')

    if user_id:
        user = User.objects.get(id=user_id)
        context = {
            'user_name': user.user_name
        }
    else:
        context = {
            'user_name': 'Khách hàng chưa đăng kí tài khoản'
        }

    return render(request, 'home.html', context)

def search(request):
    film_name = request.GET.get('film_name', '')  # Tìm kiếm phim theo tiêu đề
    genre = request.GET.get('genre', '')  # Lọc phim theo thể loại
    min_price = request.GET.get('min_price', '')  # Lọc phim theo giá tối thiểu
    max_price = request.GET.get('max_price', '')  # Lọc phim theo giá tối đa

    # Lọc phim dựa trên từ khóa tìm kiếm
    films = Film.objects.filter(film_name__icontains=film_name)

    # Lọc phim theo thể loại nếu có
    if genre:
        films = films.filter(genre__icontains=genre)

    # Lọc phim theo giá nếu có
    if min_price:
        films = films.filter(price__gte=min_price)
    if max_price:
        films = films.filter(price__lte=max_price)

    context = {
        'films': films,
        'film_name': film_name,
        'genre': genre,
        'min_price': min_price,
        'max_price': max_price,
    }
    return render(request, 'search.html', context)

def film_detail(request, film_id):
    film = Film.objects.get(id=film_id)

    if request.session.get('user_id'):
        user = User.objects.get(id=request.session.get('user_id'))
        habit, created = Habit.objects.get_or_create(user=user, film=film)
        habit.num_click += 1
        num_click = habit.num_click
        habit.save()

        context = {
            'film': film,
            'num_click': num_click,
        }
    else:
        context = {
            'film': film,
        }
        
    return render(request, 'film_detail.html', context)

def login(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')

        try:
            # Tìm kiếm người dùng theo user_name
            user = User.objects.get(user_name=user_name)

            # Kiểm tra mật khẩu
            if check_password(password, user.password):
                # Tạo session cho người dùng
                request.session['user_id'] = user.id
                messages.success(request, 'Đăng nhập thành công!')
                return redirect('home')  # Chuyển hướng đến trang home sau khi đăng nhập thành công
            else:
                messages.error(request, 'Mật khẩu không đúng.')
        except User.DoesNotExist:
            messages.error(request, 'Tên đăng nhập không đúng.')

    return render(request, 'login.html')

def logout(request):
    # Xóa tất cả dữ liệu session của người dùng
    if 'user_id' in request.session:
        del request.session['user_id']
    
    # Xóa tất cả session để đảm bảo đăng xuất hoàn toàn
    request.session.flush()

    # Chuyển hướng người dùng đến trang đăng nhập sau khi đăng xuất
    return redirect('home')

def register(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Kiểm tra các điều kiện hợp lệ
        if password != confirm_password:
            messages.error(request, 'Nhập lại mật khẩu không trùng khớp.')
            return redirect('register')
        
        if User.objects.filter(user_name=user_name).exists():
            messages.error(request, 'Tên đăng nhập đã được sử dụng.')
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Địa chỉ email đã tồn tại.')
            return redirect('register')

        # Tạo và lưu người dùng mới
        user = User(
            user_name=user_name,
            email=email,
            password=make_password(password),  # Mã hóa mật khẩu
        )
        user.save()

        request.session['user_id'] = user.id
        messages.success(request, 'Đăng ký thành công.')
        return redirect('home')
    
    return render(request, 'register.html')

def profile(request):
    if not request.session.get('user_id'):
        return redirect('login')
    user = User.objects.get(id=request.session.get('user_id'))
    context = {
        'id': user.id,
        'user_name': user.user_name,
        'email': user.email,
    }
    return render(request=request, template_name='profile.html', context=context)

def recommend(request):
    if not request.session.get('user_id'):
        return redirect('login')
    
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)

    user_habit = Habit.objects.filter(user=user)
    if not user_habit.exists():
        # Chọn ngẫu nhiên một số phim để gợi ý
        films = Film.objects.all()
        random_films = random.sample(list(films), min(5, films.count()))  # Giới hạn số lượng phim ngẫu nhiên
        context = {
            'films': random_films,
        }
    else:
        film_name_list = []
        genre_count_vector = np.zeros(len(genres))
        for habit in user_habit:
            film_name_list.append(habit.film.film_name)
            genre_list = habit.film.genre.split(',')
            for genre in genre_list:
                genre_count_vector[genres[genre]] += 1

        list_film_id = recommend_model.predict(film_name_list, genre_count_vector)
        order_case = Case(*[When(id=id_film, then=index) for index, id_film in enumerate(list_film_id)])
        films = Film.objects.filter(id__in=list_film_id).order_by(order_case)

        context = {
            'films': films,
        }
    return render(request=request, template_name='recommend.html', context=context)

def edit_profile(request):
    if not request.session.get('user_id'):
        return redirect('login')
    
    user_id = request.session.get('user_id')
    if user_id:
        user = User.objects.get(id=user_id)
    else:
        return redirect('login')  # Redirect to login if the user is not found
    
    if request.method == 'POST':
        # Lấy dữ liệu từ request.POST
        user_name = request.POST.get('user_name')
        email = request.POST.get('email')
        
        # Cập nhật các trường của user nếu có dữ liệu mới
        if user_name:
            user.user_name = user_name
        if email:
            user.email = email
        
        # Lưu các thay đổi vào database
        user.save()
        
        # Chuyển hướng về trang profile sau khi sửa xong
        return redirect('profile')
    
    # Nếu là GET request, render trang edit profile với thông tin hiện tại của user
    context = {
        'user_name': user.user_name,
        'email': user.email,
    }
    return render(request, 'edit_profile.html', context=context)