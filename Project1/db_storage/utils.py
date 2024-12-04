import logging
from django.db import transaction
from .models import Movie, Genre, Actor, Country, Ranking, MovieGenre, MovieActor

def save_movies_from_json(parsed_data):
    """
    JSON 데이터를 파싱하여 Django 데이터베이스에 저장하는 함수.
    중복 데이터 및 업데이트된 데이터를 반환.

    Args:
        parsed_data (list): 영화 데이터 리스트.

    Returns:
        dict: {'saved_movies': list, 'duplicate_movies': list, 'updated_movies': list}
    """
    saved_movies = []
    duplicate_movies = []
    updated_movies = []

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

                if created:  # 새로 저장된 영화
                    saved_movies.append(movie)
                else:  # 기존에 존재하던 영화
                    duplicate_movies.append(movie)  # 중복 영화 목록에 추가
                    updated_fields = []
                    
                    # 필드 비교 후 업데이트
                    if movie.release_year != movie_info.get('release_year', ''):
                        movie.release_year = movie_info.get('release_year', '')
                        updated_fields.append('release_year')
                    if movie.score != movie_info.get('score', 0.0):
                        movie.score = movie_info.get('score', 0.0)
                        updated_fields.append('score')
                    if movie.summary != movie_info.get('summary', ''):
                        movie.summary = movie_info.get('summary', '')
                        updated_fields.append('summary')
                    if movie.image_url != movie_info.get('image_url', ''):
                        movie.image_url = movie_info.get('image_url', '')
                        updated_fields.append('image_url')

                    if updated_fields:
                        movie.save(update_fields=updated_fields)
                        updated_movies.append(movie)  # 실제로 업데이트된 영화만 추가

                # 영화와 장르/배우 관계 추가
                for genre in genres:
                    if not MovieGenre.objects.filter(movie=movie, genre=genre).exists():
                        movie_genre_relations.append(MovieGenre(movie=movie, genre=genre))

                for actor in actors:
                    if not MovieActor.objects.filter(movie=movie, actor=actor).exists():
                        movie_actor_relations.append(MovieActor(movie=movie, actor=actor))

                # 4. 랭킹 저장
                country_code = movie_data['country_code']
                country, _ = Country.objects.get_or_create(code=country_code)
                rank = movie_data['rank']

                if not Ranking.objects.filter(country=country, movie=movie).exists():
                    ranking_relations.append(Ranking(country=country, movie=movie, rank=rank))

            # Bulk 저장
            MovieGenre.objects.bulk_create(movie_genre_relations, ignore_conflicts=True)
            MovieActor.objects.bulk_create(movie_actor_relations, ignore_conflicts=True)
            Ranking.objects.bulk_create(ranking_relations, ignore_conflicts=True)

    except Exception as e:
        logging.error(f"Error while saving movies: {e}")
        return {'saved_movies': [], 'duplicate_movies': [], 'updated_movies': []}

    logging.info(f"Successfully saved {len(saved_movies)} movies.")
    return {
        'saved_movies': saved_movies,
        'duplicate_movies': duplicate_movies,
        'updated_movies': updated_movies
    }
