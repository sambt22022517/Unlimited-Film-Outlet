from django.shortcuts import render, redirect
from .film import *

# Create your views here.
def render_all_film(request):
    return render(request, 'viewallfilm.html', {'films': get_all_film()})

def render_film(request, id_film):
    return render(request, 'viewdetailfilm.html', {'film': get_film(id_film)})