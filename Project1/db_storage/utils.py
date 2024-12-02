from rest_framework.parsers import JSONParser
from io import StringIO
from .serializers import MovieSerializer
import json

def deserialize_movie(json_string):
    """
    JSON 문자열을 입력받아 디시리얼라이즈 후 MovieSerializer로 검증 및 데이터 저장.

    Args:
        json_string (str): JSON 형식의 문자열.

    Returns:
        list: 저장된 Movie 객체 리스트 또는 오류 메시지.


        # JSON 문자열 예시
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
            print(f"Saved movie: {movie}")
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

def parse_json_file(file_path):
    """
    JSON 파일을 읽고 dict 형식으로 반환하는 함수.

    Args:
        file_path (str): JSON 파일 경로.

    Returns:
        dict: 파싱된 JSON 데이터.

    # 함수 사용 예시
    file_path = "dummy_data.json"  # JSON 파일 경로
    parsed_data = parse_json_file(file_path)

    if parsed_data:
        print(parsed_data)
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


