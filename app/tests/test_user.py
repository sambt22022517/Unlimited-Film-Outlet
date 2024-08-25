from django.test import TestCase, Client
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from django.urls import reverse
from ..models import User
import json

class LoginTestCase(TestCase):
    
    def setUp(self):
        # Tạo người dùng giả để sử dụng trong các test
        self.client = Client()
        self.password = 'password123'
        self.user = User.objects.create(
            user_name='testuser',
            password=make_password(self.password)
        )
    
    def test_login_success(self):
        # Test đăng nhập thành công
        response = self.client.post(
            reverse('login'),
            json.dumps({'user_name': 'testuser', 'password': 'password123'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': True})
    
    def test_login_user_does_not_exist(self):
        # Test khi người dùng không tồn tại
        response = self.client.post(
            reverse('login'),
            json.dumps({'user_name': 'nonexistentuser', 'password': 'password123'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': False, 'error': 'Người dùng không tồn tại'})
    
    def test_login_wrong_password(self):
        # Test khi mật khẩu không đúng
        response = self.client.post(
            reverse('login'),
            json.dumps({'user_name': 'testuser', 'password': 'wrongpassword'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': False, 'error': 'Mật khẩu không đúng'})
    
    def test_login_method_not_post(self):
        # Test khi phương thức không phải là POST
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        # Kiểm tra nếu trang login.html được render
        self.assertTemplateUsed(response, 'user/login.html')


class LogoutTestCase(TestCase):
    
    def setUp(self):
        # Tạo client để gửi các yêu cầu HTTP
        self.client = Client()
        # Đăng nhập người dùng giả để kiểm tra
        self.client.post(
            reverse('login'),
            json.dumps({'user_name': 'testuser', 'password': 'password123'}),
            content_type='application/json'
        )
    
    def test_logout_logged_in(self):
        # Đảm bảo người dùng đã đăng nhập
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Kiểm tra chuyển hướng (302)
        self.assertRedirects(response, reverse('home'))  # Kiểm tra chuyển hướng đến trang 'home'
        
        # Kiểm tra rằng session đã bị xóa
        session = self.client.session
        self.assertNotIn('user_id', session)

    def test_logout_not_logged_in(self):
        # Đăng xuất khi chưa đăng nhập
        self.client.logout()  # Xóa session hiện tại (nếu có)
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Kiểm tra chuyển hướng (302)
        self.assertRedirects(response, reverse('home'))  # Kiểm tra chuyển hướng đến trang 'home'



class RegisterTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.url = reverse('register')
    
    def test_register_success(self):
        # Test đăng ký thành công với thông tin hợp lệ
        response = self.client.post(
            self.url,
            json.dumps({
                'user_name': 'newuser',
                'email': 'newuser@example.com',
                'password': 'password123',
                'confirm_password': 'password123'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': True})
        
        # Kiểm tra rằng người dùng mới đã được tạo
        user = User.objects.get(user_name='newuser')
        self.assertIsNotNone(user)
        self.assertTrue(check_password('password123', user.password))
        self.assertEqual(self.client.session['user_id'], user.id)
    
    def test_register_password_mismatch(self):
        # Test khi mật khẩu và xác nhận mật khẩu không khớp
        response = self.client.post(
            self.url,
            json.dumps({
                'user_name': 'user1',
                'email': 'user1@example.com',
                'password': 'password123',
                'confirm_password': 'differentpassword'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': False, 'error': 'Mật khẩu nhập lại phải trùng khớp với mật khẩu ban đầu'})
    
    def test_register_username_exists(self):
        # Tạo người dùng giả để kiểm tra
        User.objects.create(
            user_name='existinguser',
            email='existinguser@example.com',
            password=make_password('password123')
        )
        
        # Test khi tên người dùng đã tồn tại
        response = self.client.post(
            self.url,
            json.dumps({
                'user_name': 'existinguser',
                'email': 'newemail@example.com',
                'password': 'password123',
                'confirm_password': 'password123'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': False, 'error': 'Tên người dùng đã được sử dụng'})
    
    def test_register_email_exists(self):
        # Tạo người dùng giả để kiểm tra
        User.objects.create(
            user_name='user2',
            email='existingemail@example.com',
            password=make_password('password123')
        )
        
        # Test khi địa chỉ email đã tồn tại
        response = self.client.post(
            self.url,
            json.dumps({
                'user_name': 'newuser2',
                'email': 'existingemail@example.com',
                'password': 'password123',
                'confirm_password': 'password123'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': False, 'error': 'Địa chỉ email đã tồn tại'})
    
    def test_register_method_not_post(self):
        # Test khi phương thức không phải là POST
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # Kiểm tra nếu trang register.html được render
        self.assertTemplateUsed(response, 'user/register.html')


class ProfileTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            user_name='testuser',
            email='testuser@example.com',
            password=make_password('password123')
        )
        self.profile_url = reverse('profile')
        self.login_url = reverse('login')

    def test_profile_logged_in(self):
        # Đăng nhập người dùng
        session = self.client.session
        session['user_id'] = self.user.id
        session.save()

        # Gửi yêu cầu GET đến trang profile
        response = self.client.get(self.profile_url)

        # Kiểm tra mã trạng thái
        self.assertEqual(response.status_code, 200)

        # Kiểm tra nếu trang profile.html được render
        self.assertTemplateUsed(response, 'user/profile.html')

        # Kiểm tra nội dung context trong trang profile
        self.assertContains(response, 'testuser')
        self.assertContains(response, 'testuser@example.com')

    def test_profile_not_logged_in(self):
        # Gửi yêu cầu GET đến trang profile khi chưa đăng nhập
        response = self.client.get(self.profile_url)

        # Kiểm tra mã trạng thái chuyển hướng (302) đến trang đăng nhập
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)


class EditProfileTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            user_name='testuser',
            email='testuser@example.com',
            password=make_password('password123')
        )
        self.existing_user = User.objects.create(
            user_name='existinguser',
            email='existinguser@example.com',
            password=make_password('password456')
        )
        self.edit_profile_url = reverse('edit_profile')
        self.login_url = reverse('login')

    def test_edit_profile_not_logged_in(self):
        # Test khi người dùng chưa đăng nhập
        response = self.client.get(self.edit_profile_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)

    def test_edit_profile_get_logged_in(self):
        # Đăng nhập người dùng
        session = self.client.session
        session['user_id'] = self.user.id
        session.save()

        # Gửi yêu cầu GET đến trang edit_profile
        response = self.client.get(self.edit_profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/edit_profile.html')
        self.assertContains(response, 'testuser')
        self.assertContains(response, 'testuser@example.com')

    def test_edit_profile_success(self):
        # Đăng nhập người dùng
        session = self.client.session
        session['user_id'] = self.user.id
        session.save()

        # Gửi yêu cầu POST với thông tin mới
        response = self.client.post(
            self.edit_profile_url,
            json.dumps({
                'user_name': 'newuser',
                'email': 'newuser@example.com'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': True, 'error': ''})

        # Kiểm tra thông tin người dùng đã được cập nhật
        self.user.refresh_from_db()
        self.assertEqual(self.user.user_name, 'newuser')
        self.assertEqual(self.user.email, 'newuser@example.com')

    def test_edit_profile_username_and_email_exists(self):
        # Đăng nhập người dùng
        session = self.client.session
        session['user_id'] = self.user.id
        session.save()

        # Gửi yêu cầu POST với tên người dùng và email đã tồn tại
        response = self.client.post(
            self.edit_profile_url,
            json.dumps({
                'user_name': 'existinguser',
                'email': 'existinguser@example.com'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': False, 'error': 'Tên người dùng và Email đã được sử dụng'})

        # Kiểm tra rằng thông tin người dùng không thay đổi
        self.user.refresh_from_db()
        self.assertEqual(self.user.user_name, 'testuser')
        self.assertEqual(self.user.email, 'testuser@example.com')