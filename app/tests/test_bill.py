from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from ..models import User, Film, Cart, Bill
import json

COMPLETE = 'P'
ERROR = 'E'
CANCELLED = 'C'
NOT_COMPLETE = 'N'

class BillTests(TestCase):
    def setUp(self):
        # Thiết lập dữ liệu dùng chung cho tất cả các test case
        self.client = Client()
        self.user = User.objects.create(user_name='testuser', email='test@example.com', password='testpassword')
        self.film = Film.objects.create(id=1, film_name='Test Film', genre=['Hành động'], price=100)
        self.cart_item = Cart.objects.create(user=self.user, film=self.film, selected=True)
        self.bill = Bill.objects.create(user=self.user, payment_date=timezone.now(), total_price=100)

    def test_render_bill_for_payment_create(self):
        # Kiểm tra chức năng tạo hóa đơn từ giỏ hàng
        session = self.client.session
        session['user_id'] = self.user.id
        session.save()

        data = {
            'total_price': 100
        }
        # Gửi yêu cầu POST để tạo hóa đơn
        response = self.client.post(reverse('render_bill_for_payment', args=['create']), json.dumps(data), content_type='application/json')

        # Kiểm tra xem phản hồi có thành công hay không và có trả về ID hóa đơn hay không
        self.assertEqual(response.status_code, 200)
        self.assertTrue('success' in response.json())
        self.assertTrue('type' in response.json())

    def test_render_bill_for_payment_buynow(self):
        # Kiểm tra chức năng mua ngay (không qua giỏ hàng)
        session = self.client.session
        session['user_id'] = self.user.id
        session.save()

        data = {
            'total_price': 100,
            'film_id': self.film.id
        }
        # Gửi yêu cầu POST để mua ngay một bộ phim
        response = self.client.post(reverse('render_bill_for_payment', args=['buynow']), json.dumps(data), content_type='application/json')

        # Kiểm tra xem phản hồi có thành công hay không và có trả về ID hóa đơn hay không
        self.assertEqual(response.status_code, 200)
        self.assertTrue('success' in response.json())
        self.assertTrue('type' in response.json())

    def test_render_bill_for_payment_view_bill(self):
        # Kiểm tra việc xem hóa đơn đã tạo
        session = self.client.session
        session['user_id'] = self.user.id
        session.save()

        # Gửi yêu cầu GET để xem hóa đơn
        response = self.client.get(reverse('render_bill_for_payment', args=[self.bill.id]))

        # Kiểm tra xem phản hồi có thành công và sử dụng đúng template không
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bill/confirm_payment.html')
        self.assertIn('films', response.context)
        self.assertIn('total_price', response.context)
        self.assertIn('bill', response.context)

    def test_render_bill(self):
        # Kiểm tra việc render trang chi tiết hóa đơn
        session = self.client.session
        session['user_id'] = self.user.id
        session.save()

        # Gửi yêu cầu GET để xem chi tiết hóa đơn
        response = self.client.get(reverse('render_bill', args=[self.bill.id]))
        
        # Kiểm tra xem phản hồi có thành công và sử dụng đúng template không
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bill/bill.html')
        self.assertIn('bill', response.context)
        self.assertIn('films', response.context)

    def test_render_bill_checkout(self):
        # Kiểm tra chức năng thanh toán hóa đơn
        session = self.client.session
        session['user_id'] = self.user.id
        session.save()

        # Gửi yêu cầu POST để thanh toán hóa đơn
        response = self.client.post(reverse('render_bill', args=[self.bill.id]), {'action': 'checkout'})
        
        # Làm mới dữ liệu hóa đơn từ database và kiểm tra trạng thái đã chuyển thành "Hoàn tất"
        self.bill.refresh_from_db()
        self.assertEqual(self.bill.status, COMPLETE)

    def test_render_bill_cancel(self):
        # Kiểm tra chức năng hủy hóa đơn
        session = self.client.session
        session['user_id'] = self.user.id
        session.save()

        # Gửi yêu cầu POST để hủy hóa đơn
        response = self.client.post(reverse('render_bill', args=[self.bill.id]), {'action': 'cancel'})
        
        # Làm mới dữ liệu hóa đơn từ database và kiểm tra trạng thái đã chuyển thành "Hủy"
        self.bill.refresh_from_db()
        self.assertEqual(self.bill.status, CANCELLED)

    def test_render_all_bill(self):
        # Kiểm tra việc render trang danh sách hóa đơn của người dùng
        session = self.client.session
        session['user_id'] = self.user.id
        session.save()

        # Gửi yêu cầu GET để xem danh sách tất cả các hóa đơn
        response = self.client.get(reverse('render_all_bill'))

        # Kiểm tra xem phản hồi có thành công và sử dụng đúng template không
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bill/all_bill.html')
        self.assertIn('bills', response.context)
        self.assertIn('user_name', response.context)
        self.assertIn('email', response.context)

    def test_render_all_bill_not_logged_in(self):
        # Kiểm tra việc chuyển hướng đến trang đăng nhập nếu người dùng chưa đăng nhập
        response = self.client.get(reverse('render_all_bill'))
        
        # Kiểm tra xem phản hồi có chuyển hướng đến trang đăng nhập không
        self.assertEqual(response.status_code, 302)  # Redirect về trang login
        self.assertRedirects(response, reverse('login'))
