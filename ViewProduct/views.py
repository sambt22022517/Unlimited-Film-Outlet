from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import Film

# Create your views here.
def ViewProduct(request):
    # return all Film
    movies = Film.objects.all()
    return render(request, "viewproduct.html", {'movies': movies})

def ViewDetail(request, movie_id):
    movie = get_object_or_404(Film, id = movie_id)
    return render(request, "viewdetail.html", {'movie': movie})

class Cart:
    pass