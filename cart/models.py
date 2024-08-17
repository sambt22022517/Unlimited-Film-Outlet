from django.db import models
from film.models import *
from user.models import *

# Create your models here.
class Cart(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    selected = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete= models.CASCADE)

    def __str__(self) -> str:
        if hasattr(self, 'user'):
            return self.user.name_user
        return "Unnamed Cart"