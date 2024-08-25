from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
from ..models import User, Film, Cart
import json

def add_cart(film, user, selected):
    num_items_in_cart = len(Cart.objects.filter(user=user))

    if Cart.objects.filter(user=user, film=film).exists():
        return (num_items_in_cart, "Đã có phim này trong giỏ hàng")
    
    Cart.objects.create(
        user=user,
        film=film,
        selected=selected
    )
    return (num_items_in_cart+1, "Thêm vào giỏ hàng thành công")

class CartTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(id=1, user_name='testuser', password='testpassword', email='test@gmail.com')
        self.film1 = Film.objects.create(id=1, film_name='Test Film 1', genre=['Hành động'], price=100)
        self.film2 = Film.objects.create(id=2, film_name='Test Film 2', genre=['Hành động'], price=100)
        self.cart_item = Cart.objects.create(user=self.user, film=self.film1, selected=False)

        self.cart_url = reverse('render_add_cart')
        self.render_get_cart_url = reverse('render_get_cart')
        self.remove_from_cart_url = reverse('remove_from_cart', args=[self.cart_item.id])
        self.select_cart_item_url = reverse('select_cart_item', args=[self.cart_item.id])

    def test_add_cart_new_item(self):
        num_items_in_cart, notification = add_cart(self.film2, self.user, True)
        self.assertEqual(num_items_in_cart, 2)
        self.assertEqual(notification, "Thêm vào giỏ hàng thành công")
        self.assertTrue(Cart.objects.filter(user=self.user, film=self.film2).exists())

    def test_add_cart_existing_item(self):
        num_items_in_cart, notification = add_cart(self.film1, self.user, True)
        self.assertEqual(num_items_in_cart, 1)
        self.assertEqual(notification, "Đã có phim này trong giỏ hàng")

    def test_render_add_cart_not_logged_in(self):
        response = self.client.post(self.cart_url, data=json.dumps({'film_id': self.film1.id}), content_type='application/json')
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertRedirects(response, reverse('login'))

    def test_render_get_cart_logged_in(self):
        session = self.client.session
        session['user_id'] = self.user.id
        session.save()

        response = self.client.get(self.render_get_cart_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/cart.html')

        response_data = response.context
        self.assertEqual(response_data['user_name'], self.user.user_name)
        self.assertEqual(response_data['email'], self.user.email)
        self.assertEqual(response_data['num_items_in_cart'], 1)
        self.assertTrue(response_data['user_logged_in'])
        self.assertIn('carts', response_data)

    def test_render_get_cart_not_logged_in(self):
        response = self.client.get(self.render_get_cart_url)
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertRedirects(response, reverse('login'))

    def test_remove_from_cart_logged_in(self):
        session = self.client.session
        session['user_id'] = self.user.id
        session.save()

        response = self.client.delete(self.remove_from_cart_url)
        self.assertEqual(response.status_code, 200)
        
        response_data = response.json()
        self.assertTrue(response_data['success'])
        self.assertEqual(response_data['num_items_in_cart'], 0)
        self.assertFalse(Cart.objects.filter(id=self.cart_item.id).exists())

    def test_remove_from_cart_not_logged_in(self):
        response = self.client.delete(self.remove_from_cart_url)
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertRedirects(response, reverse('login'))

    def test_remove_from_cart_invalid_method(self):
        session = self.client.session
        session['user_id'] = self.user.id
        session.save()

        response = self.client.get(self.remove_from_cart_url)
        self.assertEqual(response.status_code, 404)  # Method not allowed

    def test_select_cart_item_post(self):
        session = self.client.session
        session['user_id'] = self.user.id
        session.save()

        response = self.client.post(self.select_cart_item_url, data=json.dumps({'selected': True}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
        response_data = response.json()
        self.assertTrue(response_data['success'])
        self.cart_item.refresh_from_db()
        self.assertTrue(self.cart_item.selected)

    def test_select_cart_item_invalid_method(self):
        response = self.client.get(self.select_cart_item_url)
        self.assertEqual(response.status_code, 404)  # Method not allowed
        response_data = response.json()
        self.assertFalse(response_data['success'])
        self.assertEqual(response_data['error'], "Method phải là POST")
