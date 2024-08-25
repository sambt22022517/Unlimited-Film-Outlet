import json
from django.http import JsonResponse
from ..models import User
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password

def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_name = data.get('user_name')
        password = data.get('password')

        try:
            # Tìm kiếm người dùng theo user_name
            user = User.objects.get(user_name=user_name)

            # Kiểm tra mật khẩu
            if check_password(password, user.password):
                # Tạo session cho người dùng
                request.session['user_id'] = user.id
                return JsonResponse({'success': True})  # Đăng nhập thành công
            else:
                return JsonResponse({'success': False, 'error': 'Mật khẩu không đúng'})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Người dùng không tồn tại'})

    return render(request, 'user/login.html')

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
        data = json.loads(request.body)
        user_name = data.get('user_name')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        
        # Kiểm tra các điều kiện hợp lệ
        if password != confirm_password:
            return JsonResponse({'success': False, 'error': 'Mật khẩu nhập lại phải trùng khớp với mật khẩu ban đầu'})
        
        if User.objects.filter(user_name=user_name).exists():
            return JsonResponse({'success': False, 'error': 'Tên người dùng đã được sử dụng'})
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'error': 'Địa chỉ email đã tồn tại'})

        # Tạo và lưu người dùng mới
        user = User(
            user_name=user_name,
            email=email,
            password=make_password(password),  # Mã hóa mật khẩu
        )
        user.save()

        request.session['user_id'] = user.id
        return JsonResponse({'success': True})  # Đăng ký thành công
    
    return render(request, 'user/register.html')

def profile(request):
    if not request.session.get('user_id'):
        return redirect('login')
    user = User.objects.get(id=request.session.get('user_id'))
    context = {
        'user_name': user.user_name,
        'email': user.email,
        'user_logged_in': True,
    }
    return render(request=request, template_name='user/profile.html', context=context)

def edit_profile(request):    
    user_id = request.session.get('user_id')
    if user_id:
        user = User.objects.get(id=user_id)
    else:
        return redirect('login')  # Redirect to login if the user is not found
    
    if request.method == 'POST':
        data = json.loads(request.body)
        user_name = data.get('user_name')
        email = data.get('email')
        
        response_data = {'success': True, 'error':''}
        if user_name and email:
            user_exist = User.objects.filter(user_name=user_name).exists()
            email_exist = User.objects.filter(email=email).exists()

            if user_exist and email_exist:
                response_data['success'] = False
                response_data['error'] += 'Tên người dùng và Email đã được sử dụng'
            elif not user_exist and email_exist:
                user.user_name = user_name
            elif user_exist and not email_exist:
                user.email = email
            else:
                user.user_name = user_name
                user.email = email

        user.save()
        
        return JsonResponse(response_data)
    
    # Nếu là GET request, render trang edit profile với thông tin hiện tại của user
    context = {
        'user_name': user.user_name,
        'email': user.email,
    }
    return render(request, 'user/edit_profile.html', context=context)