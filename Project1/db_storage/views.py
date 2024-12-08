import os
import json
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import save_movies_from_json  # utils.py에서 함수 호출

JSON_PATH = '../WebCrawling/data/raw/movies_data_country.json'
logger = logging.getLogger(__name__)

class BulkInsertRankingView(APIView):
    def post(self, request, *args, **kwargs):
        # JSON 파일 경로 설정
        file_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), JSON_PATH                
        )
        try:

            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            movies_data = data.get('movies', [])
            if not movies_data:
                return Response({"error": "No movie data provided."}, status=status.HTTP_400_BAD_REQUEST)
            
            # save_movies_from_json 함수 호출, 여기서 데이터 저장
            saved_movies = save_movies_from_json(movies_data)

            saved_movies = result['saved_movies']
            duplicate_movies = result['duplicate_movies']
            updated_movies = result['updated_movies']

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
            return Response({"error": "JSON file not found."}, status=status.HTTP_404_NOT_FOUND)
        except json.JSONDecodeError:
            logger.error("Error decoding JSON file.")
            return Response({"error": "Error decoding JSON file."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error saving movies: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
