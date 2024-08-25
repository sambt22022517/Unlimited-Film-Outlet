from django.test import TestCase
from django.urls import reverse
from ..models import Film, Cart, User
from ..serializers import FilmSerializer

class HomeViewTest(TestCase):
    def setUp(self):
        # Tạo người dùng và phim mẫu
        self.user = User.objects.create(user_name='testuser', password='testpassword')
        self.film1 = Film.objects.create(
            id='t51234',
            film_name='Sample Film 1',
            story='Sample Description',
            price=20000,
            genre=['Chính kịch', 'Hài kịch', 'Thời sự']
        )
        self.film2 = Film.objects.create(
            id='t51235',
            film_name='Sample Film 2',
            story='Sample Description',
            price=20000,
            genre=['Kinh dị', 'Hài kịch', 'Hành động']
        )
        
        # URL của trang home
        self.home_url = reverse('home')

    def test_home_not_logged_in(self):
        # Xóa hết mọi thứ trong session trước khi kiểm tra
        self.client.session.flush()
        
        # Gửi yêu cầu GET đến trang home mà không đăng nhập
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/home.html')

        # Kiểm tra response data khi chưa đăng nhập
        self.assertEqual(response.context['user_logged_in'], False)
        self.assertEqual(response.context['user_name'], '')
        self.assertEqual(response.context['num_items_in_cart'], 0)

        # Kiểm tra phim trong context
        films = Film.objects.order_by('-release_date')[:20]
        serializer = FilmSerializer(films, many=True, context={'request': response.wsgi_request})
        self.assertEqual(response.context['films'], serializer.data)

    def test_home_logged_in(self):
        # Đăng nhập người dùng
        session = self.client.session
        session['user_id'] = self.user.id
        session.save()

        # Tạo một giỏ hàng với phim đã chọn
        Cart.objects.create(user=self.user, film=self.film1, selected=True)

        # Gửi yêu cầu GET đến trang home
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/home.html')

        # Kiểm tra response data
        self.assertEqual(response.context['user_logged_in'], True)
        self.assertEqual(response.context['user_name'], 'testuser')

        # Kiểm tra số lượng phim đã chọn trong giỏ hàng của người dùng
        num_items_in_cart = Cart.objects.filter(user=self.user, selected=True).count()
        self.assertEqual(response.context['num_items_in_cart'], num_items_in_cart)

        # Kiểm tra phim trong context
        films = Film.objects.order_by('-release_date')[:20]
        serializer = FilmSerializer(films, many=True, context={'request': response.wsgi_request})
        self.assertEqual(response.context['films'], serializer.data)
