from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from .models import User, Film, Habit
from django.contrib.messages import get_messages


class LoginViewTest(TestCase):

    def setUp(self):
        # Tạo một người dùng test
        self.user = User.objects.create(
            user_name='testuser',
            password=make_password('testpassword')
        )
        self.client = Client()
        self.login_url = reverse('login')  # Giả sử URL đăng nhập được đặt là 'login'
        self.home_url = reverse('home')  # Giả sử URL trang home là 'home'

    def test_login_success(self):
        # Kiểm tra đăng nhập thành công
        response = self.client.post(self.login_url, {
            'user_name': 'testuser',
            'password': 'testpassword',
        })
        # Kiểm tra chuyển hướng đến trang home sau khi đăng nhập thành công
        self.assertRedirects(response, self.home_url)
        # Kiểm tra session có lưu ID người dùng
        self.assertEqual(int(self.client.session['user_id']), self.user.id)

    def test_login_user_does_not_exist(self):
        # Gửi POST request với tên đăng nhập không tồn tại
        response = self.client.post(self.login_url, {
            'user_name': 'nonexistentuser',
            'password': 'testpassword',
        })
        messages = list(get_messages(response.wsgi_request))
        # Kiểm tra thông báo lỗi có xuất hiện trong messages
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Tên đăng nhập không đúng.')

    def test_login_wrong_password(self):
        # Kiểm tra khi mật khẩu không đúng
        response = self.client.post(self.login_url, {
            'user_name': 'testuser',
            'password': 'wrongpassword',
        })
        messages = list(get_messages(response.wsgi_request))
        # Kiểm tra thông báo lỗi có xuất hiện trong messages
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Mật khẩu không đúng.')

    def test_login_without_post(self):
        # Kiểm tra khi gửi GET request (không phải POST)
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')


class IndexViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.index_url = reverse('index')  # Giả sử URL của trang index là 'index'
        self.login_url = reverse('login')  # Giả sử URL của trang login là 'login'

    def test_redirect_if_not_logged_in(self):
        # Kiểm tra chuyển hướng đến trang đăng nhập nếu chưa đăng nhập
        response = self.client.get(self.index_url)
        self.assertRedirects(response, self.login_url)

    def test_render_index_if_logged_in(self):
        # Giả lập việc người dùng đã đăng nhập bằng cách thiết lập session
        session = self.client.session
        session['user_id'] = 1  # Thiết lập user_id tùy ý (1 chỉ là ví dụ)
        session.save()

        # Kiểm tra việc render trang index khi người dùng đã đăng nhập
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


class HomeViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(user_name='testuser', password='testpassword')
        self.home_url = reverse('home')

    def test_home_no_login(self):
        # Kiểm tra khi người dùng chưa đăng nhập
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, 'Khách hàng chưa đăng kí tài khoản')

    def test_home_logged_in(self):
        # Giả lập người dùng đã đăng nhập bằng cách thiết lập session
        session = self.client.session
        session['user_id'] = self.user.id
        session.save()

        # Kiểm tra khi người dùng đã đăng nhập
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, self.user.user_name)  # Kiểm tra tên người dùng hiển thị đúng


class SearchViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.search_url = reverse('search')  # Giả sử URL của trang tìm kiếm là 'search'

        # Tạo một số phim mẫu để test
        self.film1 = Film.objects.create(
            film_name='Công viên lỏng khung',
            genre='Action, Drama',
            price=10,
            story='Bộ phim về một khu công viên bị thiếu kinh phí khi xây dựng.'
        )
        self.film2 = Film.objects.create(
            film_name='Thuỷ thủ chặt măng',
            genre='Comedy, Horror, Action',
            price=15,
            story='Bộ phim về những người thuỷ thủ lạc vào một hòn đảo chỉ có một rừng tre.'
        )
        self.film3 = Film.objects.create(
            film_name='Cây tre đâm chốt',
            genre='Drama, Animation',
            price=20,
            story='Bộ phim về một cây tre vi phạm luật giao thông.'
        )

    def test_search_by_title(self):
        # Tìm kiếm phim theo tiêu đề
        response = self.client.get(self.search_url, {'film_name': 'Công viên'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.film1.film_name)
        self.assertNotContains(response, self.film2.film_name)
        self.assertNotContains(response, self.film3.film_name)

    def test_filter_by_genre(self):
        # Lọc phim theo thể loại
        response = self.client.get(self.search_url, {'genre': 'Comedy'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.film2.film_name)
        self.assertNotContains(response, self.film1.film_name)
        self.assertNotContains(response, self.film3.film_name)

    def test_filter_by_price_range(self):
        # Lọc phim theo khoảng giá
        response = self.client.get(self.search_url, {'min_price': 15, 'max_price': 20})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.film2.film_name)
        self.assertContains(response, self.film3.film_name)
        self.assertNotContains(response, self.film1.film_name)

    def test_search_with_combined_filters(self):
        # Tìm kiếm với điều kiện kết hợp
        response = self.client.get(self.search_url, {'film_name': 'măng', 'genre': 'Action', 'min_price': 5, 'max_price': 15})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.film1.film_name)
        self.assertContains(response, self.film2.film_name)
        self.assertNotContains(response, self.film3.film_name)

    def test_search_with_no_result(self):
        # Tìm kiếm với điều kiện kết hợp
        response = self.client.get(self.search_url, {'film_name': 'lỏng', 'genre': 'Horror', 'min_price': 18, 'max_price': 25})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.film1.film_name)
        self.assertNotContains(response, self.film2.film_name)
        self.assertNotContains(response, self.film3.film_name)


class FilmDetailViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(user_name='testuser', password='testpassword')
        self.film = Film.objects.create(film_name='Sample Film', genre='Action', price=10)
        self.film_detail_url = reverse('film_detail', args=[self.film.id])

    def test_film_detail_no_login(self):
        # Kiểm tra khi người dùng chưa đăng nhập
        response = self.client.get(self.film_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'film_detail.html')
        self.assertContains(response, self.film.film_name)
        self.assertNotIn('num_click', response.context)  # Không có 'num_click' trong context khi chưa đăng nhập

    def test_film_detail_logged_in(self):
        # Giả lập người dùng đã đăng nhập bằng cách thiết lập session
        session = self.client.session
        session['user_id'] = self.user.id
        session.save()

        # Kiểm tra lần đầu tiên truy cập
        response = self.client.get(self.film_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'film_detail.html')
        self.assertContains(response, self.film.film_name)
        self.assertEqual(response.context['num_click'], 1)  # Kiểm tra num_click được ghi nhận lần đầu

        # Kiểm tra lần thứ hai truy cập
        response = self.client.get(self.film_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['num_click'], 2)  # Kiểm tra num_click tăng lên

        # Kiểm tra Habit được tạo và cập nhật đúng cách
        habit = Habit.objects.get(user=self.user, film=self.film)
        self.assertEqual(habit.num_click, 2)


class LogoutViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(user_name='testuser', password='testpassword')
        self.home_url = reverse('home')
        self.logout_url = reverse('logout')

        # Giả lập người dùng đã đăng nhập
        session = self.client.session
        session['user_id'] = self.user.id
        session.save()

    def test_logout(self):
        # Kiểm tra xem người dùng có đăng xuất thành công không
        response = self.client.get(self.logout_url)
        
        # Kiểm tra xem session đã bị xóa
        self.assertNotIn('user_id', self.client.session)

        # Kiểm tra xem người dùng có được chuyển hướng đến trang chủ
        self.assertRedirects(response, self.home_url)


class RegisterViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.home_url = reverse('home')

    def test_register_success(self):
        data = {
            'user_name': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123',
            'confirm_password': 'password123',
        }
        response = self.client.post(self.register_url, data)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().user_name, 'newuser')
        self.assertRedirects(response, self.home_url)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Đăng ký thành công.')

    def test_register_password_mismatch(self):
        data = {
            'user_name': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123',
            'confirm_password': 'password456',
        }
        response = self.client.post(self.register_url, data)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Nhập lại mật khẩu không trùng khớp.')

    def test_register_user_name_taken(self):
        User.objects.create(user_name='existinguser', email='existinguser@example.com', password='password123')
        data = {
            'user_name': 'existinguser',
            'email': 'newemail@example.com',
            'password': 'password123',
            'confirm_password': 'password123',
        }
        response = self.client.post(self.register_url, data)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Tên đăng nhập đã được sử dụng.')

    def test_register_email_taken(self):
        User.objects.create(user_name='anotheruser', email='existingemail@example.com', password='password123')
        data = {
            'user_name': 'newuser',
            'email': 'existingemail@example.com',
            'password': 'password123',
            'confirm_password': 'password123',
        }
        response = self.client.post(self.register_url, data)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Địa chỉ email đã tồn tại.')


class ProfileViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            user_name='testuser',
            email='testuser@example.com',
            password='password123',
        )
        self.profile_url = reverse('profile')
        self.login_url = reverse('login')

    def test_profile_not_logged_in(self):
        # Kiểm tra khi người dùng chưa đăng nhập
        response = self.client.get(self.profile_url)
        self.assertRedirects(response, self.login_url)

    def test_profile_logged_in(self):
        # Đăng nhập người dùng
        session = self.client.session
        session['user_id'] = self.user.id
        session.save()

        # Kiểm tra khi người dùng đã đăng nhập
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.user_name)
        self.assertContains(response, self.user.email)


class RecommendViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            user_name='testuser',
            email='testuser@example.com',
            password='password123',
        )
        self.film1 = Film.objects.create(film_name='Film 1', genre='Hành động', price=10)
        self.film2 = Film.objects.create(film_name='Film 2', genre='Hài kịch', price=10)
        self.habit = Habit.objects.create(user=self.user, film=self.film1, num_click=5)
        self.recommend_url = reverse('recommend')
        self.login_url = reverse('login')

    def test_recommend_not_logged_in(self):
        # Kiểm tra khi người dùng chưa đăng nhập
        response = self.client.get(self.recommend_url)
        self.assertRedirects(response, self.login_url)

    def test_recommend_logged_in(self):
        # Đăng nhập người dùng
        session = self.client.session
        session['user_id'] = self.user.id
        session.save()

        # Kiểm tra khi người dùng đã đăng nhập và có thói quen xem phim
        response = self.client.get(self.recommend_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.film1.film_name)

    def test_recommend_no_habits_random_films(self):
        # Đăng nhập người dùng nhưng không có thói quen xem phim
        Habit.objects.all().delete()
        session = self.client.session
        session['user_id'] = self.user.id
        session.save()

        response = self.client.get(self.recommend_url)
        self.assertEqual(response.status_code, 200)
        
        # Kiểm tra xem có bất kỳ phim nào được gợi ý ngẫu nhiên không
        self.assertContains(response, self.film1.film_name)
        self.assertContains(response, self.film2.film_name)


class EditProfileViewTest(TestCase):

    def setUp(self):
        # Tạo một người dùng mẫu để sử dụng trong các test
        self.user = User.objects.create(
            user_name='testuser',
            email='test@example.com',
            password='testpassword'
        )

        self.edit_profile_url = reverse('edit_profile')
        self.profile_url = reverse('profile')
        self.login_url = reverse('login')

    def test_edit_profile_get(self):
        """
        Kiểm tra yêu cầu GET tới trang chỉnh sửa profile.
        Xác nhận rằng trang trả về đúng thông tin người dùng hiện tại.
        """
        session = self.client.session
        session['user_id'] = self.user.id
        session.save()

        response = self.client.get(self.edit_profile_url)
        self.assertEqual(response.status_code, 200)  # Kiểm tra xem yêu cầu có thành công không
        self.assertContains(response, 'testuser')    # Kiểm tra xem tên người dùng có hiển thị đúng không
        self.assertContains(response, 'test@example.com')  # Kiểm tra xem email có hiển thị đúng không

    def test_edit_profile_post(self):
        """
        Kiểm tra yêu cầu POST tới trang chỉnh sửa profile.
        Xác nhận rằng thông tin người dùng được cập nhật và chuyển hướng đúng.
        """
        session = self.client.session
        session['user_id'] = self.user.id
        session.save()

        response = self.client.post(self.edit_profile_url, {
            'user_name': 'newuser',
            'email': 'new@example.com',
        })
        # Làm mới thông tin người dùng từ database để kiểm tra các thay đổi
        self.user.refresh_from_db()
        self.assertEqual(self.user.user_name, 'newuser')  # Kiểm tra xem tên người dùng có được cập nhật không
        self.assertEqual(self.user.email, 'new@example.com')  # Kiểm tra xem email có được cập nhật không
        self.assertRedirects(response, self.profile_url)  # Kiểm tra xem người dùng có được chuyển hướng về trang profile không

    def test_edit_profile_no_login(self):
        """
        Kiểm tra trường hợp người dùng chưa đăng nhập.
        Xác nhận rằng người dùng chưa đăng nhập sẽ bị chuyển hướng đến trang đăng nhập.
        """
        response = self.client.get(self.edit_profile_url)
        self.assertRedirects(response, self.login_url)  # Kiểm tra xem người dùng có bị chuyển hướng đến trang đăng nhập không