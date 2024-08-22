from ..models import User, Film, Habit, Cart
from ..ml_model import RecommendModel
from ..serializers import FilmSerializer
from django.shortcuts import render, redirect
import json
import random
import numpy as np
import pandas as pd
from django.db.models import Case, When
from django.http import JsonResponse

recommend_model = RecommendModel()
genres = {
    "Chính kịch": 0,
    "Âm nhạc": 1,
    "Nhạc kịch": 2,
    "Giả tưởng": 3,
    "Hành động": 4,
    "Phiêu lưu": 5,
    "Hài kịch": 6,
    "Bí ẩn": 7,
    "Khoa học viễn tưởng": 8,
    "Phim ngắn": 9,
    "Kinh dị tâm lý": 10,
    "Kinh dị": 11,
    "Tiểu sử": 12,
    "Thể thao": 13,
    "Lãng mạn": 14,
    "Gia đình": 15,
    "Lịch sử": 16,
    "Hoạt hình": 17,
    "Tài liệu": 18,
    "Hình sự": 19,
    "Chiến tranh": 20,
    "Miền Tây hoang dã": 21,
    "Trực tiếp": 22,
    "Trò chơi truyền hình": 23,
    "Thoại mục": 24,
    "Tin tức": 25,
    "Phim người lớn": 26,
}

def search(request):
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

    film_name = request.GET.get('film_name', '')  # Tìm kiếm phim theo tiêu đề
    genres_on_id = [int(key) for key, value in request.GET.items() if value == "on"]  # Lọc phim theo thể loại
    min_price = request.GET.get('min', '')  # Lọc phim theo giá tối thiểu
    max_price = request.GET.get('max', '')  # Lọc phim theo giá tối đa

    # Lọc phim dựa trên từ khóa tìm kiếm
    films = Film.objects.filter(film_name__icontains=film_name)

    # Lọc phim theo thể loại nếu có

    if genres_on_id:
        for idx in genres_on_id:
            genre = list(genres.keys())[idx]
            films = films.filter(genre__icontains=genre)

    # Lọc phim theo giá nếu có
    if min_price:
        films = films.filter(price__gte=min_price)
    if max_price:
        films = films.filter(price__lte=max_price)
        
    films = films[:20]
    serializer = FilmSerializer(films, many=True, context={'request': request})

    list_genre = [{'id': idx, 'genre': genre, 'on': False} for idx, genre in enumerate(genres.keys())]
    for idx in genres_on_id:
        list_genre[idx]['on'] = True

    response_data.update({
        'films': serializer.data,
        'film_name': film_name,
        'min_price': min_price,
        'max_price': max_price,
        'genres': list_genre,
    })
    return render(request, 'filter/search.html', response_data)

def recommend(request):    
    user_id = request.session.get('user_id')

    if user_id:
        user = User.objects.get(id=user_id)
    else:
        return redirect('login')
    
    num_items_in_cart = len(Cart.objects.filter(user=user))
    response_data = {
        'user_name': user.user_name,
        'num_items_in_cart': num_items_in_cart,
        'user_logged_in': True,
    }

    if request.method == 'GET':
        genres_on_id = [int(key) for key, value in request.GET.items() if value == "on"]
        min_price = request.GET.get('min', '')
        max_price = request.GET.get('max', '')

    elif request.method == 'POST':
        data = json.loads(request.body)
        genres_on_id = data.get('genres')
        min_price = data.get('min', '')
        max_price = data.get('max', '')

        films = Film.objects.all()
        for idx in genres_on_id:
            genre = list(genres.keys())[int(idx)]
            films = films.filter(genre__icontains=genre)
        if min_price:
            films = films.filter(price__gte=min_price)
        if max_price:
            films = films.filter(price__lte=max_price)

        
        if len(films) > 0:
            user_habit = Habit.objects.filter(user=user)
            if not user_habit.exists():
                # Chọn ngẫu nhiên một số phim để gợi ý
                films = random.sample(list(films), min(20, films.count()))
            else:
                film_id_list = []
                genre_count_vector = np.zeros(len(genres))
                for habit in user_habit:
                    film_id_list.append(habit.film.id)
                    genre_list = habit.film.genre
                    for genre in genre_list:
                        genre_count_vector[genres[genre]] += 1
                
                # Chuyển đổi danh sách các từ điển thành DataFrame
                data = list(films.values())
                df = pd.DataFrame(data)
                df['film_id'] = df['id']
                df['genre'] = df['genre'].apply(lambda x: ', '.join(x))

                list_film_id = recommend_model.predict(df, film_id_list, genre_count_vector)
                order_case = Case(*[When(id=id_film, then=index) for index, id_film in enumerate(list_film_id)])
                films = Film.objects.filter(id__in=list_film_id).order_by(order_case)
        serializer = FilmSerializer(films, many=True, context={'request': request})
            
        response_data.update({
            'success': True,
            'films': serializer.data,
        })
        return JsonResponse(response_data, status=200)

    list_genre = [{'id': idx, 'genre': genre, 'on': False} for idx, genre in enumerate(genres.keys())]
    for idx in genres_on_id:
        list_genre[idx]['on'] = True

    response_data.update({
        'min_price': min_price,
        'max_price': max_price,
        'genres': list_genre,
    })
    return render(request=request, template_name='filter/recommend.html', context=response_data)