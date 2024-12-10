from rest_framework import serializers
from .models import Country, Genre, Actor, Movie, Ranking

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['id', 'name']


class MovieSerializer(serializers.ModelSerializer):
    genres = serializers.ListField(child=serializers.CharField())
    actors = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = Movie
        fields = ['id', 'title', 'release_year', 'score', 'summary', 'image_url', 'genres', 'actors']


class RankingSerializer(serializers.Serializer):
    name = serializers.CharField(source='country.name', max_length=10)
    movie = MovieSerializer()
    rank = serializers.IntegerField()
