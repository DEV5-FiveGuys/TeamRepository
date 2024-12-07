from decimal import Decimal
import logging
from django.db import transaction
from .models import Movie, Genre, Actor, Country, Ranking, MovieGenre, MovieActor

def save_movies_from_json(parsed_data: list) -> dict:
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
                # score null 처리
                score = movie_info.get('score', 0.0)
                if not score or score == 'null':
                    score = Decimal(0)
                movie, created = Movie.objects.get_or_create(
                    title=movie_info['title'],
                    defaults={
                        'release_year': movie_info.get('release_year', ''),
                        'score': score,
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
                    # 소수점 1자리까지 반올림하여 비교 => float형 부동소수점 비교때문에
                    # 에러 있어서 round 삭제
                    if movie.score != score:
                        movie.score = score
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
                country_name = movie_data['country']
                country, _ = Country.objects.get_or_create(name=country_name)
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
    
def get_movies_by_country_name(name: str) -> list[dict]:
    '''
    국가 이름에 따라 1~5위 영화를 반환
    
    Args:
        name: 국가 이름
    Returns:
        moivies: 1~5위 영화의 정보를 담은 리스트
    
    '''
    try:
        country = Country.objects.filter(name__iexact=name).first() # 국가를 DB에서 get
        if not country:
            return {'status_code': 404, 'method': 'get_movies_by_country_name', 'error': f'{name} does not exist'}
        # 랭킹 데이터를 1~5위 까지 get
        rankings = (
            Ranking.objects.filter(country = country)
            .select_related('movie')
            .order_by('rank')[:5]
        ) 
        # 데이터를 list[dict] 형태로 변환
        movies = []
        for ranking in rankings:
            movie = ranking.movie
            movies.append({
                "rank": ranking.rank,
                "title": movie.title,
                "release_year": movie.release_year,
                "score": float(movie.score),
                "summary": movie.summary,
                "image": movie.image_url,
                "genres": list(movie.genres.values_list("name", flat=True)),
                "actors": list(movie.actors.values_list("name", flat=True)),       
            })
        return movies if movies else {'status_code': 500, 'method': 'get_movies_by_country_name', 'error': 'movies list is empty'} 
    
    except Exception as e:
        return {'status_code': 500, 'method': 'get_movies_by_country_name', 'error': str(e)}
