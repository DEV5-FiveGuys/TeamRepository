import logging
import json
from django.db import transaction
from .models import Movie, Genre, Actor, Country, Ranking, MovieGenre, MovieActor

def save_movies_from_json(parsed_data):
    """
    JSON 데이터를 파싱하여 Django 데이터베이스에 저장하는 함수.
    중복 데이터 처리를 추가하고, 에러 로깅 기능을 포함.

    Args:
        parsed_data (list): 영화 데이터 리스트.

    Returns:
        list: 저장된 Movie 객체 리스트.
    """
    saved_movies = []

    try:
        # 트랜잭션 시작
        with transaction.atomic():
            movie_genre_relations = []
            movie_actor_relations = []
            ranking_relations = []

            for movie_data in parsed_data:
                # 1. 장르 저장
                genres = []
                for genre_name in movie_data['movie'].get('genres', []):
                    genre, _ = Genre.objects.get_or_create(name=genre_name)
                    genres.append(genre)

                # 2. 배우 저장
                actors = []
                for actor_name in movie_data['movie'].get('actors', []):
                    actor, _ = Actor.objects.get_or_create(name=actor_name)
                    actors.append(actor)

                # 3. 영화 저장
                movie_info = movie_data['movie']
                movie, created = Movie.objects.get_or_create(
                    title=movie_info['title'],
                    defaults={
                        'release_year': movie_info.get('release_year', ''),
                        'score': movie_info.get('score', 0.0),
                        'summary': movie_info.get('summary', ''),
                        'image_url': movie_info.get('image_url', ''),
                    }
                )

                if created:
                    # 영화와 장르의 관계를 설정
                    for genre in genres:
                        if not MovieGenre.objects.filter(movie=movie, genre=genre).exists():
                            movie_genre_relations.append(MovieGenre(movie=movie, genre=genre))

                    # 영화와 배우의 관계를 설정
                    for actor in actors:
                        if not MovieActor.objects.filter(movie=movie, actor=actor).exists():
                            movie_actor_relations.append(MovieActor(movie=movie, actor=actor))

                # 4. 랭킹 저장
                country_code = movie_data['country_code']
                country, _ = Country.objects.get_or_create(code=country_code)
                rank = movie_data['rank']

                if not Ranking.objects.filter(country=country, movie=movie).exists():
                    ranking_relations.append(Ranking(country=country, movie=movie, rank=rank))

                saved_movies.append(movie)

            # Bulk 저장
            MovieGenre.objects.bulk_create(movie_genre_relations, ignore_conflicts=True)
            MovieActor.objects.bulk_create(movie_actor_relations, ignore_conflicts=True)
            Ranking.objects.bulk_create(ranking_relations, ignore_conflicts=True)

    except Exception as e:
        logging.error(f"Error while saving movies: {e}")
        return []

    logging.info(f"Successfully saved {len(saved_movies)} movies.")
    return saved_movies
