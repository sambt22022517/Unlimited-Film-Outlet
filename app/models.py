from django.db import models
from datetime import datetime

class User(models.Model):
    user_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    total_click = models.PositiveIntegerField(default=0)

class Genre(models.Model):
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
    name = models.CharField(max_length=100, unique=True, choices=option)

class Film(models.Model):
    film_name = models.CharField(max_length=255)  # Tiêu đề của bộ phim
    cover = models.ImageField(upload_to='covers/', blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)  # Đạo diễn
    actor = models.CharField(max_length=4096, blank=True, null=True)  # Diễn viên
    genre = models.ManyToManyField(Genre, related_name='films')  # Thể loại
    release_date = models.IntegerField(default=datetime.now().year)  # Ngày phát hành
    story = models.TextField(blank=True, null=True)  # Mô tả (có thể để trống)
    rating = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)  # Đánh giá (có thể để trống)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Giá phim

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Người dùng nhấp chuột
    film = models.ForeignKey(Film, on_delete=models.CASCADE)  # Bộ phim được nhấp chuột
    num_click = models.PositiveIntegerField(default=0)  # Số lần nhấp chuột