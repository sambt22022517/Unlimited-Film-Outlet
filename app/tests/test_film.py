from django.test import TestCase, Client
from django.urls import reverse
from ..models import User, Film, Habit, Cart
from ..serializers import FilmSerializer
from django.contrib.auth.hashers import make_password

class FilmDetailViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            user_name='testuser',
            email='testuser@example.com',
            password=make_password('password123')
        )
        self.film = Film.objects.create(
            id='t51234',
            film_name='Sample Film',
            story='Sample Description',
            price=20000,
            genre=['Chính kịch', 'Hài kịch', 'Thời sự']
        )
        self.film_detail_url = reverse('film_detail', kwargs={'film_id': self.film.id})

    def test_film_detail_not_logged_in(self):
        # Test khi người dùng chưa đăng nhập
        response = self.client.get(self.film_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'film/film_detail.html')

        # Kiểm tra response data
        self.assertEqual(response.context['user_logged_in'], False)
        self.assertIn('film', response.context)
        serializer = FilmSerializer(self.film, many=False, context={'request': response.wsgi_request})
        self.assertEqual(response.context['film'], serializer.data)

    def test_film_detail_logged_in(self):
        # Đăng nhập người dùng
        session = self.client.session
        session['user_id'] = self.user.id
        session.save()

        # Tạo một giỏ hàng với phim đã chọn
        Cart.objects.create(user=self.user, film=self.film, selected=True)

        # Gửi yêu cầu GET đến trang film_detail
        response = self.client.get(self.film_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'film/film_detail.html')

        # Kiểm tra response data
        self.assertEqual(response.context['user_logged_in'], True)
        self.assertEqual(response.context['user_name'], 'testuser')

        # Kiểm tra số lượng phim đã chọn trong giỏ hàng của người dùng
        num_items_in_cart = Cart.objects.filter(user=self.user, selected=True).count()
        self.assertEqual(response.context['num_items_in_cart'], num_items_in_cart)

        # Kiểm tra phim trong context
        self.assertIn('film', response.context)
        serializer = FilmSerializer(self.film, many=False, context={'request': response.wsgi_request})
        self.assertEqual(response.context['film'], serializer.data)

        # Kiểm tra num_click được cập nhật đúng
        habit = Habit.objects.get(user=self.user, film=self.film)
        self.assertEqual(habit.num_click, 1)

    def test_film_detail_habit_increment(self):
        # Đăng nhập người dùng
        session = self.client.session
        session['user_id'] = self.user.id
        session.save()

        # Tạo một habit trước đó
        habit = Habit.objects.create(user=self.user, film=self.film, num_click=5)

        # Gửi yêu cầu GET đến trang film_detail
        response = self.client.get(self.film_detail_url)
        self.assertEqual(response.status_code, 200)

        # Kiểm tra num_click đã tăng lên
        habit.refresh_from_db()
        self.assertEqual(habit.num_click, 6)

    def test_film_detail_habit_creation(self):
        # Đăng nhập người dùng
        session = self.client.session
        session['user_id'] = self.user.id
        session.save()

        # Gửi yêu cầu GET đến trang film_detail mà không có habit trước đó
        response = self.client.get(self.film_detail_url)
        self.assertEqual(response.status_code, 200)

        # Kiểm tra habit được tạo mới với num_click là 1
        habit = Habit.objects.get(user=self.user, film=self.film)
        self.assertEqual(habit.num_click, 1)
