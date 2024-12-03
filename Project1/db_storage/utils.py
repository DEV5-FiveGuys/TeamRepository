from rest_framework.parsers import JSONParser
from io import StringIO
from .serializers import MovieSerializer
import json
import logging
from django.db import transaction
from .models import Country, Genre, Actor, Movie, MovieGenre, MovieActor, Ranking

def deserialize_movie(json_string):
    """
    JSON 문자열을 입력받아 디시리얼라이즈 후 MovieSerializer로 검증 및 데이터 저장.

    Args:
        json_string (str): JSON 형식의 문자열.

    Returns:
        list: 저장된 Movie 객체 리스트 또는 오류 메시지.
    """
    try:
        # JSON 문자열을 파싱하여 Python 객체로 변환
        stream = StringIO(json_string)
        data = JSONParser().parse(stream)

        # 여러 개의 데이터를 처리하기 위해 리스트 형태로 가정
        if isinstance(data, list):
            saved_movies = []
            for item in data:
                serializer = MovieSerializer(data=item)
                if serializer.is_valid():
                    movie = serializer.save()  # DB에 저장
                    saved_movies.append(movie)
                else:
                    print(f"Validation error: {serializer.errors}")
            return saved_movies
        else:
            # 단일 데이터 처리
            serializer = MovieSerializer(data=data)
            if serializer.is_valid():
                return serializer.save()  # DB에 저장
            else:
                print(f"Validation error: {serializer.errors}")
                return None
    except Exception as e:
        print(f"Error during deserialization: {e}")
        return None

"""# JSON 문자열 예시
json_string = 
[
    {
        "title": "오징어 게임",
        "year": "2021–2025",
        "score": "8.0",
        "summary": "Hundreds of cash-strapped players accept a strange invitation...",
        "country": "KR",
        "genre": ["Action", "Drama", "Mystery"],
        "stars": ["Lee Jung-jae", "Park Hae-soo", "Nandito Hidayattullah Putra"],
        "rank": 1
    },
    {
        "title": "Mr. Peullangkeuton",
        "year": "2024",
        "score": "8.2",
        "summary": "A man with little chance for happiness...",
        "country": "KR",
        "genre": ["Comedy", "Romance"],
        "stars": ["Woo Do-Hwan", "Lee Yoo-mi", "Oh Jung-se"],
        "rank": 2
    }
]


# 함수 호출
saved_movies = deserialize_movie(json_string)

if saved_movies:
    for movie in saved_movies:
        print(f"Saved movie: {movie}")"""



def parse_json_file(file_path):
    """
    JSON 파일을 읽고 dict 형식으로 반환하는 함수.

    Args:
        file_path (str): JSON 파일 경로.

    Returns:
        dict: 파싱된 JSON 데이터.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: 파일 {file_path}을(를) 찾을 수 없습니다.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: JSON 파싱 오류가 발생했습니다. {e}")
        return None

"""# 함수 사용 예시
file_path = "dummy_data.json"  # JSON 파일 경로
parsed_data = parse_json_file(file_path)

if parsed_data:
    print(parsed_data)"""



# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('movie_import.log'),
        logging.StreamHandler()
    ]
)

def save_movies_from_json(json_string):
    """
    JSON 데이터를 파싱하여 Django 데이터베이스에 저장하는 함수.
    중복 데이터 처리를 추가하고, 에러 로깅 기능을 포함.

    Args:
        json_string (str): JSON 형식의 문자열.

    Returns:
        list: 저장된 Movie 객체 리스트.
    """
    data = json.loads(json_string)
    saved_movies = []

    try:
        # 트랜잭션 시작
        with transaction.atomic():
            movie_genre_relations = []
            movie_actor_relations = []
            ranking_relations = []

            for movie_data in data:
                # 1. 장르 저장
                genres = []
                for genre_name in movie_data.get('genres', []):
                    genre, _ = Genre.objects.get_or_create(name=genre_name)
                    genres.append(genre)

                # 2. 배우 저장
                actors = []
                for actor_name in movie_data.get('actors', []):
                    actor, _ = Actor.objects.get_or_create(name=actor_name)
                    actors.append(actor)

                # 3. 영화 저장
                movie, created = Movie.objects.get_or_create(
                    title=movie_data['title'],
                    defaults={
                        'release_year': movie_data.get('release_year', ''),
                        'score': movie_data.get('score', 0.0),
                        'summary': movie_data.get('summary', ''),
                        'image_url': movie_data.get('image_url', ''),
                    }
                )

                if created:
                    for genre in genres:
                        if not MovieGenre.objects.filter(movie=movie, genre=genre).exists():
                            movie_genre_relations.append(MovieGenre(movie=movie, genre=genre))

                    for actor in actors:
                        if not MovieActor.objects.filter(movie=movie, actor=actor).exists():
                            movie_actor_relations.append(MovieActor(movie=movie, actor=actor))

                # 4. 랭킹 저장
                for ranking_data in movie_data.get('ranking', []):
                    country_code = ranking_data.get('country')
                    rank = ranking_data.get('rank')

                    # 국가 저장
                    country, _ = Country.objects.get_or_create(code=country_code)

                    if not Ranking.objects.filter(country=country, rank=rank).exists():
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

"""
모듈 사용 방법
파일 저장 위치

apps/movies/utils/json_parser.py로 저장.
사용 시 호출

views.py에서 아래처럼 임포트 후 호출합니다.

from .utils.json_parser import save_movies_from_json

def import_movies_view(request):
    json_string =
    [
        {
            "title": "오징어 게임",
            "release_year": "2021",
            "score": 8.0,
            "summary": "A thrilling survival game...",
            "image_url": "https://example.com/image1.jpg",
            "genres": ["Action", "Drama"],
            "actors": ["Lee Jung-jae", "Park Hae-soo"],
            "ranking": [{"country": "KR", "rank": 1}]
        }
    ]

    saved_movies = save_movies_from_json(json_string)
    return JsonResponse({"message": f"Saved {len(saved_movies)} movies"})
"""