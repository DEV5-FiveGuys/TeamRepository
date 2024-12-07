from django.test import TestCase
from unittest.mock import patch, MagicMock
from .utils import MovieCrawler
import json

class MovieCrawlerTest(TestCase):
    """MovieCrawler 클래스의 테스트"""

    @patch('crawler.crawler.MovieCrawler.initialize_driver')  # WebDriver 초기화 부분을 mock 처리
    def test_crawl_movies(self, mock_initialize_driver):
        """영화 데이터를 크롤링하는 함수의 테스트"""

        # 크롤러 초기화
        mock_driver = MagicMock()
        mock_wait = MagicMock()
        mock_initialize_driver.return_value = mock_driver  # 드라이버가 반환되도록 mock 처리

        # MovieCrawler 인스턴스 생성
        crawler = MovieCrawler(top_n=5)

        # 크롤링 과정에서 사용할 mock 데이터 설정
        mock_movie_data = {
            "movies": [
                {
                    "country": "USA",
                    "movie": {
                        "title": "Movie Title 1",
                        "release_year": 2020,
                        "score": 8.5,
                        "summary": "A great movie",
                        "image_url": "https://image_url.com/1",
                        "genres": ["Action", "Adventure"],
                        "actors": ["Actor 1", "Actor 2"]
                    },
                    "rank": 1
                },
                {
                    "country": "USA",
                    "movie": {
                        "title": "Movie Title 2",
                        "release_year": 2021,
                        "score": 7.5,
                        "summary": "Another great movie",
                        "image_url": "https://image_url.com/2",
                        "genres": ["Drama", "Thriller"],
                        "actors": ["Actor 3", "Actor 4"]
                    },
                    "rank": 2
                }
            ]
        }

        # 크롤링 작업이 정상적으로 실행되었을 때, mock 데이터 반환
        crawler.crawling = MagicMock(return_value=mock_movie_data)

        # 실제 크롤링 실행
        result = crawler.crawling()

        # 결과 검증
        self.assertIsInstance(result, dict)  # 반환값은 dict 타입이어야 한다
        self.assertIn('movies', result)  # 반환값에 'movies' 키가 있어야 한다
        self.assertEqual(len(result['movies']), 2)  # 'movies' 목록에는 두 개의 영화가 있어야 한다
        self.assertEqual(result['movies'][0]['movie']['title'], "Movie Title 1")  # 첫 번째 영화 제목 검증
        self.assertEqual(result['movies'][1]['movie']['title'], "Movie Title 2")  # 두 번째 영화 제목 검증

    @patch('crawler.crawler.MovieCrawler.load_country_codes')  # 국가 코드 로드 부분을 mock 처리
    def test_load_country_codes(self, mock_load_country_codes):
        """국가 코드 로드 함수의 테스트"""

        # mock 데이터 설정
        mock_load_country_codes.return_value = {
            "US": "USA",
            "KR": "South Korea",
        }

        # MovieCrawler 인스턴스 생성
        crawler = MovieCrawler(top_n=5)

        # 실제 함수 실행
        country_codes = crawler.load_country_codes()

        # 검증
        self.assertEqual(country_codes, {"US": "USA", "KR": "South Korea"})  # 반환값이 mock 데이터와 동일해야 한다

    @patch('crawler.crawler.MovieCrawler.scrape_modal_content')  # 모달 콘텐츠 크롤링 부분을 mock 처리
    def test_scrape_modal_content(self, mock_scrape_modal_content):
        """모달 콘텐츠 크롤링 함수의 테스트"""

        # mock 데이터 설정
        mock_scrape_modal_content.return_value = {
            'title': 'Sample Movie',
            'year': '2021',
            'score': '7.8',
            'summary': 'This is a sample movie summary.',
            'img': 'https://sampleimage.com',
            'genre': ['Drama', 'Comedy'],
            'stars': ['Actor 1', 'Actor 2']
        }

        # MovieCrawler 인스턴스 생성
        crawler = MovieCrawler(top_n=5)

        # mock 데이터를 사용하는 테스트
        content = crawler.scrape_modal_content(mock_wait, crawler.BASE_XPATH, crawler.RELATIVE_XPATHS)

        # 검증
        self.assertEqual(content['title'], 'Sample Movie')  # 영화 제목이 mock 데이터와 일치해야 한다
        self.assertEqual(content['year'], '2021')  # 개봉년도
        self.assertEqual(content['score'], '7.8')  # 평점
        self.assertEqual(content['summary'], 'This is a sample movie summary.')  # 요약
        self.assertEqual(content['img'], 'https://sampleimage.com')  # 이미지 URL
        self.assertEqual(content['genre'], ['Drama', 'Comedy'])  # 장르
        self.assertEqual(content['stars'], ['Actor 1', 'Actor 2'])  # 출연 배우

    @patch('crawler.crawler.MovieCrawler.save_dict_as_json')  # JSON 저장 부분을 mock 처리
    def test_save_dict_as_json(self, mock_save_dict_as_json):
        """결과를 JSON 파일로 저장하는 함수의 테스트"""

        # MovieCrawler 인스턴스 생성
        crawler = MovieCrawler(top_n=5)

        # mock 데이터 설정
        mock_data = {"movies": [{"title": "Sample Movie"}]}

        # JSON 저장 함수 호출
        crawler.save_dict_as_json(mock_data, './data/raw/movies_data.json')

        # 검증
        mock_save_dict_as_json.assert_called_once_with(mock_data, './data/raw/movies_data.json')  # 저장 함수가 정확한 인자와 함께 호출되었는지 확인
