from django.test import TestCase, Client
from django.urls import reverse
from ..models import User, Film, Cart, Habit
from ..serializers import FilmSerializer
import json
from unittest.mock import patch

class SearchViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(user_name='testuser', email='test@example.com', password='testpassword')
        self.film1 = Film.objects.create(id='t5678', film_name='Film A', price=10.0, genre=['Chính kịch'])
        self.film2 = Film.objects.create(id='t5679', film_name='Film B', price=20.0, genre=['Hài kịch'])
        self.search_url = reverse('search')

    def test_search_not_logged_in(self):
        response = self.client.get(self.search_url, {'film_name': 'Film A'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'filter/search.html')

        # Kiểm tra rằng người dùng chưa đăng nhập
        self.assertFalse(response.context['user_logged_in'])
        self.assertEqual(response.context['user_name'], '')
        self.assertEqual(response.context['num_items_in_cart'], 0)

        # Kiểm tra kết quả tìm kiếm
        serializer = FilmSerializer([self.film1], many=True, context={'request': response.wsgi_request})
        self.assertEqual(response.context['films'], serializer.data)

    def test_search_logged_in(self):
        # Đăng nhập người dùng
        session = self.client.session
        session['user_id'] = self.user.id
        session.save()

        Cart.objects.create(user=self.user, film=self.film1)

        response = self.client.get(self.search_url, {'film_name': 'Film A'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'filter/search.html')

        # Kiểm tra rằng người dùng đã đăng nhập
        self.assertTrue(response.context['user_logged_in'])
        self.assertEqual(response.context['user_name'], 'testuser')
        self.assertEqual(response.context['num_items_in_cart'], 1)

        # Kiểm tra kết quả tìm kiếm
        serializer = FilmSerializer([self.film1], many=True, context={'request': response.wsgi_request})
        self.assertEqual(response.context['films'], serializer.data)

    def test_search_by_genre(self):
        response = self.client.get(self.search_url, {'0': 'on'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'filter/search.html')

        # Kiểm tra kết quả tìm kiếm theo thể loại
        serializer = FilmSerializer([self.film1], many=True, context={'request': response.wsgi_request})
        self.assertEqual(response.context['films'], serializer.data)

    def test_search_by_price(self):
        response = self.client.get(self.search_url, {'min': '15', 'max': '25'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'filter/search.html')

        # Kiểm tra kết quả tìm kiếm theo giá
        serializer = FilmSerializer([self.film2], many=True, context={'request': response.wsgi_request})
        self.assertEqual(response.context['films'], serializer.data)