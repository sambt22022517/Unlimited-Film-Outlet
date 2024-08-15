from django.db import models

class User(models.Model):
    user_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

class Film(models.Model):
    film_name = models.CharField(max_length=255)  # Tiêu đề của bộ phim
    cover = models.ImageField(upload_to='covers/', blank=True, null=True)
    author = models.CharField(max_length=255)  # Đạo diễn
    actor = models.CharField(max_length=255)  # Diễn viên
    genre = models.CharField(max_length=100)  # Thể loại
    release_date = models.DateField()  # Ngày phát hành
    story = models.TextField(blank=True, null=True)  # Mô tả (có thể để trống)
    rating = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)  # Đánh giá (có thể để trống)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Giá phim

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Người dùng nhấp chuột
    film = models.ForeignKey(Film, on_delete=models.CASCADE)  # Bộ phim được nhấp chuột
    num_click = models.PositiveIntegerField(default=0)  # Số lần nhấp chuột