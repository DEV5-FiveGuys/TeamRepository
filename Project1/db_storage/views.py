import os
import json
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from db_storage.utils import *  # utils.py에서 함수 호출
from db_storage.models import *
from visualizations.visualizer import Visualizer

# JSON 파일 경로를 절대 경로로 설정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(BASE_DIR, 'crawler', 'data', 'raw', 'movies_data_country.json')

logger = logging.getLogger(__name__)

class BulkInsertRankingView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # JSON 파일 읽기
            with open(JSON_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)

            movies_data = data.get('movies', [])
            if not movies_data:
                return Response({"error": "No movie data provided."}, status=status.HTTP_400_BAD_REQUEST)
            
            # save_movies_from_json 함수 호출, 여기서 데이터 저장
            result = save_movies_from_json(movies_data)
            
            saved_movies = result['saved_movies']
            duplicate_movies = result['duplicate_movies']
            updated_movies = result['updated_movies']
            
            if not saved_movies:
                return Response({"error": "Empty saved_movies."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    "message": f"{len(saved_movies)} movies saved successfully.",
                    "details": {
                        "saved_movies_count": len(saved_movies),
                        "duplicate_movies_count": len(duplicate_movies),
                        "updated_movies_count": len(updated_movies),
                    },
                    "saved_movies": [movie.title for movie in saved_movies],
                    "duplicate_movies": [movie.title for movie in duplicate_movies],
                    "updated_movies": [movie.title for movie in updated_movies],
                }, status=status.HTTP_201_CREATED)

        except FileNotFoundError:
            logger.error("JSON file not found.")
            return Response({"error": f"File not found: {JSON_PATH}"}, status=status.HTTP_404_NOT_FOUND)
        except json.JSONDecodeError:
            logger.error("Error decoding JSON file.")
            return Response({"error": "Error decoding JSON file."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error saving movies: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetMovieListByCountryAPIView(APIView):
    def get(self, request, country_name) -> Response:
        # URL 또는 Query Parameter에서 'country_name' 가져오기

        if not country_name:
            return Response({"error": "Required: country_name"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            movies = get_movies_by_country_name(country_name)
            if not movies:
                return Response({
                    "error": f"No movies found for country: {country_name}"}, status=status.HTTP_404_NOT_FOUND
                ) # TODO: Validation Visualizer로 이전
            # visualizer 
            visualizer = Visualizer(country_name=country_name)
            visualizer.visualize_TOPK(k=5)
            visualizer.visualize_wordcloud(display_type='html', colormap='magma')
            visualizer.visualize_piechart(k=8)
            visualizer.visualize_average_rating()
            return Response({'message': 'success'})
            
        except Exception as e:
           return Response(
                {"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) 