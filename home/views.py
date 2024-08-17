from django.shortcuts import render
from user.models import *

# Create your views here.
def render_home(request):
    try:
        id_user = request.session['id_user']
        user = User.objects.get(id = id_user)
        return render(request, 'home.html',{'user': user})
    except:
        return render(request, 'home.html')