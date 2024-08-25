from django.test import TestCase, Client
from django.urls import reverse
from ..models import User
from django.contrib.auth.hashers import make_password

class IndexViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            user_name='testuser',
            email='testuser@example.com',
            password=make_password('password123')
        )
        self.index_url = reverse('index')
        self.login_url = reverse('login')

    def test_index_not_logged_in(self):
        # Test khi người dùng chưa đăng nhập
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)

    def test_index_logged_in(self):
        # Đăng nhập người dùng
        session = self.client.session
        session['user_id'] = self.user.id
        session.save()

        # Gửi yêu cầu GET đến trang index
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index/index.html')
