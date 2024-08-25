from ..models import User, Film, Habit, Cart
from ..serializers import FilmSerializer
from django.shortcuts import render

def film_detail(request, film_id):
    film = Film.objects.get(id=film_id)

    user_id = request.session.get('user_id')
    if user_id:
        user = User.objects.get(id=user_id)

        habit, created = Habit.objects.get_or_create(user=user, film=film)
        habit.num_click += 1
        num_click = habit.num_click
        habit.save()

        num_items_in_cart = len(Cart.objects.filter(user=user))
        response_data = {
            'user_name': user.user_name,
            'num_items_in_cart': num_items_in_cart,
            'user_logged_in': True,
        }
    else:
        response_data = {
            'user_logged_in': False,
        }
    
    serializer = FilmSerializer(film, many=False, context={'request': request})
    response_data.update({
        'film': serializer.data,
    })
        
    return render(request, 'film/film_detail.html', response_data)