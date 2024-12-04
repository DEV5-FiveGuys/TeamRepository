from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import logging
from .utils import save_movies_from_json  # utils.py에서 함수 호출
from django.http import JsonResponse

logger = logging.getLogger(__name__)

class BulkInsertRankingView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data  # 요청 데이터 받아오기
        movies_data = data.get('movies', [])  # 'movies' 항목을 가져옵니다.

        if not movies_data:
            return Response({"error": "No movie data provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # save_movies_from_json 함수 호출
            result = save_movies_from_json(movies_data)

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

        except Exception as e:
            logger.error(f"Error saving movies: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
