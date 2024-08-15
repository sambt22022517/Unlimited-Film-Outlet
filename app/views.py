from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Film, Habit
from .ml_model import RecommendModel
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Case, When

recommend_model = RecommendModel()

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
        return redirect('login')  # Chuyển hướng đến trang đăng nhập nếu người dùng chưa đăng nhập

    return render(request, 'home.html', context)

def search(request):
    query = request.GET.get('q', '')  # Tìm kiếm phim theo tiêu đề
    genre = request.GET.get('genre', '')  # Lọc phim theo thể loại
    min_price = request.GET.get('min_price', '')  # Lọc phim theo giá tối thiểu
    max_price = request.GET.get('max_price', '')  # Lọc phim theo giá tối đa

    # Lọc phim dựa trên từ khóa tìm kiếm
    films = Film.objects.filter(film_name__icontains=query)

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
        'query': query,
        'genre': genre,
        'min_price': min_price,
        'max_price': max_price,
    }
    return render(request, 'search.html', context)

def film_detail(request, film_id):
    film = Film.objects.get(id=film_id)
    user = User.objects.get(id=request.session.get('user_id'))

    if request.session.get('user_id'):
        habit, created = Habit.objects.get_or_create(user=user, film=film)
        habit.num_click += 1
        num_click = habit.num_click
        habit.save()

    context = {
        'film': film,
        'num_click': num_click,
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
            messages.error(request, 'Tên đăng nhập  không đúng.')

    return render(request, 'login.html')

def logout(request):
    # Xóa tất cả dữ liệu session của người dùng
    if 'user_id' in request.session:
        del request.session['user_id']
    
    # Xóa tất cả session để đảm bảo đăng xuất hoàn toàn
    request.session.flush()

    # Chuyển hướng người dùng đến trang đăng nhập sau khi đăng xuất
    return redirect('login')

def register(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Kiểm tra các điều kiện hợp lệ
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')
        
        if User.objects.filter(user_name=user_name).exists():
            messages.error(request, 'User_name already taken.')
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already in use.')
            return redirect('register')

        # Tạo và lưu người dùng mới
        user = User(
            user_name=user_name,
            email=email,
            password=make_password(password),  # Mã hóa mật khẩu
        )
        user.save()

        request.session['user_id'] = user.id
        messages.success(request, 'Registration successful! You can now log in.')
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

    list_film_id = recommend_model.predict(user_habit)
    order_case = Case(*[When(id=id_film, then=index) for index, id_film in enumerate(list_film_id)])
    films = Film.objects.filter(id__in=list_film_id).order_by(order_case)

    context = {
        'films': films,
    }
    return render(request=request, template_name='recommend.html', context=context)
