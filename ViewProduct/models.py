from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=1000)
    def __str__(self) -> str:
        return self.name
    
class Actor(models.Model):
    name = models.CharField(max_length=1000)
    def __str__(self) -> str:
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=1000)
    def __str__(self) -> str:
        return self.name
    
class Film(models.Model):
    name = models.CharField(max_length=1000)
    cover = models.CharField(max_length=1000)

    author = models.ManyToManyField(Author) #
    actor = models.ManyToManyField(Actor) #
    genre = models.ManyToManyField(Genre) #

    story = models.TextField()
    rating = models.DecimalField(
        max_digits=4,
        decimal_places=2
    )
    release_date = models.DateField()

    def __str__(self) -> str:
        return self.name