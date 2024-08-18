from django.db import models
from datetime import datetime
from multiselectfield import MultiSelectField

class User(models.Model):
    user_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    total_click = models.PositiveIntegerField(default=0)

option = [
    ("Chính kịch", "Chính kịch"),
    ("Âm nhạc", "Âm nhạc"),
    ("Nhạc kịch", "Nhạc kịch"),
    ("Giả tưởng", "Giả tưởng"),
    ("Hành động", "Hành động"),
    ("Phiêu lưu", "Phiêu lưu"),
    ("Hài kịch", "Hài kịch"),
    ("Bí ẩn", "Bí ẩn"),
    ("Khoa học viễn tưởng", "Khoa học viễn tưởng"),
    ("Phim ngắn", "Phim ngắn"),
    ("Kinh dị tâm lý", "Kinh dị tâm lý"),
    ("Kinh dị", "Kinh dị"),
    ("Tiểu sử", "Tiểu sử"),
    ("Thể thao", "Thể thao"),
    ("Lãng mạn", "Lãng mạn"),
    ("Gia đình", "Gia đình"),
    ("Lịch sử", "Lịch sử"),
    ("Hoạt hình", "Hoạt hình"),
    ("Tài liệu", "Tài liệu"),
    ("Hình sự", "Hình sự"),
    ("Chiến tranh", "Chiến tranh"),
    ("Miền Tây hoang dã", "Miền Tây hoang dã"),
    ("Trực tiếp", "Trực tiếp"),
    ("Trò chơi truyền hình", "Trò chơi truyền hình"),
    ("Thoại mục", "Thoại mục"),
    ("Tin tức", "Tin tức"),
    ("Phim người lớn", "Phim người lớn"),
]

class Film(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    film_name = models.CharField(max_length=255)  # Tiêu đề của bộ phim
    cover = models.ImageField(upload_to='covers/', blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)  # Đạo diễn
    actor = models.CharField(max_length=4096, blank=True, null=True)  # Diễn viên
    genre = MultiSelectField(choices=option, blank=True, null=True)  # Thể loại
    release_date = models.IntegerField(default=datetime.now().year)  # Ngày phát hành
    story = models.TextField(blank=True, null=True)  # Mô tả (có thể để trống)
    rating = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)  # Đánh giá (có thể để trống)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Giá phim

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Người dùng nhấp chuột
    film = models.ForeignKey(Film, on_delete=models.CASCADE)  # Bộ phim được nhấp chuột
    num_click = models.PositiveIntegerField(default=0)  # Số lần nhấp chuột

class Cart(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    selected = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete= models.CASCADE)

    def __str__(self) -> str:
        if hasattr(self, 'user'):
            return self.user.user_name
        return "Unnamed Cart"
    
class Bill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(default=datetime.now())

    COMPLETE = 'P'
    ERROR = 'E'
    CANCELLED = 'C'
    NOT_COMPLETE = 'N'

    # hoàn thành
    # bị hủy
    # lỗi (Không thanh toán được)

    ORDER_STATUS_CHOICES = [
        (COMPLETE, 'Complete'),
        (ERROR, 'Error'),
        (CANCELLED, 'Cancelled'),
        (NOT_COMPLETE, 'Not Complete'),
    ]
    status = models.CharField(
        max_length=2,
        choices=ORDER_STATUS_CHOICES,
        default=NOT_COMPLETE
    )
    total_price = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True
    )
    def __str__(self) -> str:
        return str(self.payment_date)

class BillItem(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.film.film_name