from .models import *
from django.shortcuts import get_object_or_404

def get_all_film():
    films = Film.objects.all()
    return films
def get_film(id_film):
    film = get_object_or_404(Film, id = id_film)
    return film