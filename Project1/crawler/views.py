from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import MovieCrawler  # MovieCrawler 클래스 import

class CrawlMoviesView(APIView):
    """영화 크롤링을 트리거하는 APIView"""

    def get(self, request, *args, **kwargs):
        """
        영화 정보를 크롤링하여 JSON 형식으로 반환합니다.
        예를 들어, `GET /api/crawl_movies/` 요청 시 영화 데이터를 크롤링하여 반환합니다.
        """
        try:
            # 크롤러 인스턴스 생성
            crawler = MovieCrawler(top_n=10)
            # 영화 크롤링 실행
            result = crawler.crawling()

            # 크롤링된 결과 반환
            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            # 오류 발생 시 500 Internal Server Error 반환
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
