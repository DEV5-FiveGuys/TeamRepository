from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import Country, Genre, Actor, Movie, Ranking
from .serializers import *

class BulkInsertRankingView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = RankingSerializer(data=data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    # 1. Get or create the country
                    country_code = serializer.validated_data['country_code']
                    country, _ = Country.objects.get_or_create(code=country_code)

                    # 2. Process movie, genres, and actors
                    movie_data = serializer.validated_data['movie']
                    genres = movie_data.pop('genres')
                    actors = movie_data.pop('actors')

                    movie, _ = Movie.objects.get_or_create(
                        title = movie_data['title'],
                        release_year = movie_data['release_year'].split('-')[0],
                        score = movie_data['score'],
                        summary = movie_data['summary'],
                        image_url =  movie_data['image_url'],
                    )

                    # 3. Handle genres and MovieGenre
                    genre_instances = []
                    for genre_name in genres:
                        genre, _ = Genre.objects.get_or_create(name=genre_name)
                        genre_instances.append(genre)
                    movie.genres.set(genre_instances)

                    # 4. Handle actors and MovieActor
                    actor_instances = []
                    for actor_name in actors:
                        actor, _ = Actor.objects.get_or_create(name=actor_name)
                        actor_instances.append(actor)
                    movie.actors.set(actor_instances)
                    
                    # movie.genres.set([Genre.objects.get_or_create(name=genre)[0] for genre in genres])
                    # movie.actors.set([Actor.objects.get_or_create(name=actor)[0] for actor in actors])

                    # 5. Create ranking
                    rank = serializer.validated_data['rank']
                    Ranking.objects.create(country=country, movie=movie, rank=rank)

                return Response({'message': 'Bulk insert successful'}, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
