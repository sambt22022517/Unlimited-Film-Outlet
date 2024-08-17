from django.db import models

# Create your models here.
class User(models.Model):
    user_name = models.CharField(max_length=255, unique= True)
    email = models.CharField(max_length=255, unique = True)
    password = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.user_name