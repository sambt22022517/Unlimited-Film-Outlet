from ..models import User, Film, Cart
from ..serializers import FilmSerializer
from django.shortcuts import render

def home(request):
    user_id = request.session.get('user_id')

    if user_id:
        user = User.objects.get(id=user_id)
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

    films = Film.objects.order_by('-release_date')[:20]
    serializer = FilmSerializer(films, many=True, context={'request': request})

    response_data.update({
        'films': serializer.data,
    })

    return render(request=request, template_name='home/home.html', context=response_data)