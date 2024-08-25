from rest_framework import serializers
from .models import Film, Cart

class FilmSerializer(serializers.ModelSerializer):
    imageUrl = serializers.SerializerMethodField()
    genre = serializers.SerializerMethodField()

    class Meta:
        model = Film
        fields = ['id', 'film_name', 'imageUrl', 'author', 'actor', 'genre', 'release_date', 'story', 'rating', 'price']

    def get_imageUrl(self, obj):
        request = self.context.get('request')
        if obj.cover and request:
            return request.build_absolute_uri(obj.cover.url)
        return None

    def get_genre(self, obj):
        return ", ".join(obj.genre)

class CartSerializer(serializers.ModelSerializer):
    film = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'film', 'selected']

    def get_film(self, obj):
        request = self.context.get('request')
        return FilmSerializer(obj.film, many=False, context={'request': request}).data
