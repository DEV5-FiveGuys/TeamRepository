from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import Country, Genre, Actor, Movie, Ranking
from .serializers import RankingSerializer  # 필요에 따라 직렬화기 임포트

class BulkInsertRankingView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        # 'movies'가 리스트로 전달되는 구조에 맞추어 처리
        movies_data = data.get('movies', [])
        
        if not movies_data:
            return Response({"error": "No movie data provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                for movie_data in movies_data:
                    # country_code, rank, and movie data 처리
                    country_code = movie_data['country_code']
                    country, _ = Country.objects.get_or_create(code=country_code)

                    # Movie 데이터 처리
                    movie_info = movie_data['movie']
                    genres = movie_info.pop('genres')
                    actors = movie_info.pop('actors')
                    movie, _ = Movie.objects.get_or_create(
                        title=movie_info['title'],
                        release_year=movie_info['release_year'].split('–')[0],
                        defaults={
                            'score': movie_info['score'],
                            'summary': movie_info['summary'],
                            'image_url': movie_info['image_url'],
                        },
                    )
                    # Genres, Actors 처리
                    movie.genres.set([Genre.objects.get_or_create(name=genre)[0] for genre in genres])
                    movie.actors.set([Actor.objects.get_or_create(name=actor)[0] for actor in actors])

                    # Ranking 생성
                    rank = movie_data['rank']
                    Ranking.objects.create(country=country, movie=movie, rank=rank)

                return Response({'message': 'Bulk insert successful'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)