from django.db import models

# Create your models here.
class Film(models.Model):
    film_name = models.CharField(max_length=255)
    cover = models.CharField(max_length=255)# Image Field

    author = models.CharField(max_length=255) #
    actor = models.CharField(max_length=255) #
    genre = models.CharField(max_length=255) #

    story = models.TextField()
    rating = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null= True
    )

    release_date = models.DateField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True
    )

    def __str__(self) -> str:
        return self.film_name