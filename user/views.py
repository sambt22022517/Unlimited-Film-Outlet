from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .user import *
# Create your views here.

def render_register(request):
    if request.method == "POST":
        user_name = request.POST.get("user_name")
        password = request.POST.get("password")
        repeat_password = request.POST.get("repeat_password")
        email = request.POST.get("email")

        state, notification = register(user_name, password, repeat_password, email)
        if state == 'True':
            return redirect("Login")
        else:
            return render(request, "register.html", {'state': state, 'notification': notification})
    return render(request, "register.html")

def render_login(request):
    if request.method == "POST":
        user_name = request.POST.get("user_name")
        password = request.POST.get("password")

        state, notification = login(user_name, password)
        if state == 'True':
            request.session['id_user'] = User.objects.get(user_name = user_name).id
            return redirect("Home")
        else:
            return render(request, "login.html", {'state': state, 'notification': notification})

    return render(request, "login.html")

def render_logout(request):
    if 'id_user' in request.session:
        del request.session['id_user']
    return redirect("Home")

def render_info(request):
    pass
