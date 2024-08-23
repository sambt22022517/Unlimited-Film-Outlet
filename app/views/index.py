from django.shortcuts import render, redirect

def index(request):
    if not request.session.get('user_id'):
        return redirect('login')
    return render(request=request, template_name='index/index.html')