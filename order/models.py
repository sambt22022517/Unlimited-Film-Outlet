from django.db import models
from user.models import *
from film.models import *

# Create your models here.
class Bill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_date = models.DateTimeField()

    COMPLETE = 'P'
    ERROR = 'E'
    CANCELLED = 'C'

    # hoàn thành
    # bị hủy
    # lỗi (Không thanh toán được)

    ORDER_STATUS_CHOICES = [
        (COMPLETE, 'Complete'),
        (ERROR, 'Error'),
        (CANCELLED, 'Cancelled'),
    ]
    status = models.CharField(
        max_length=2,
        choices=ORDER_STATUS_CHOICES,
        default=COMPLETE
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
