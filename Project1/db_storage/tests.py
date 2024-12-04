from decimal import Decimal
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import Country, Genre, Actor, Movie, Ranking

"""class BulkInsertRankingViewTest(APITestCase):
    
    # URL을 테스트 전에 설정합니다.
    def setUp(self):
        self.url = reverse('bulk-insert-ranking')  # 뷰의 실제 URL 이름을 여기에 입력하세요.
    
    # 유효한 영화 데이터
    def valid_payload(self):
        return {
            "movies": [
                {
                    "country_code": "KR",
                    "movie": {
                        "title": "오징어 게임",
                        "release_year": "2021–2025",
                        "score": "8.0",
                        "summary": "Hundreds of cash-strapped players accept a strange invitation to compete in children's games.",
                        "image_url": "https://example.com/image.jpg",
                        "genres": ["Action", "Drama", "Mystery"],
                        "actors": ["Lee Jung-jae", "Park Hae-soo", "Nandito Hidayattullah Putra"]
                    },
                    "rank": 1
                },
                {
                    "country_code": "US",
                    "movie": {
                        "title": "Inception",
                        "release_year": "2010",
                        "score": "8.8",
                        "summary": "A thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea.",
                        "image_url": "https://example.com/inception.jpg",
                        "genres": ["Sci-Fi", "Action", "Thriller"],
                        "actors": ["Leonardo DiCaprio", "Joseph Gordon-Levitt", "Elliot Page"]
                    },
                    "rank": 2
                },
                {
                    "country_code": "IN",
                    "movie": {
                        "title": "RRR",
                        "release_year": "2022",
                        "score": "8.2",
                        "summary": "A fictitious story about two legendary revolutionaries and their journey away from home.",
                        "image_url": "https://example.com/rrr.jpg",
                        "genres": ["Action", "Drama"],
                        "actors": ["N.T. Rama Rao Jr.", "Ram Charan", "Alia Bhatt"]
                    },
                    "rank": 3
                }
            ]
        }

    def test_bulk_insert_multiple_movies(self):
        # 유효한 페이로드로 POST 요청을 보냅니다.
        response = self.client.post(self.url, self.valid_payload(), format='json')

        # 응답 코드가 201 CREATED인지 확인합니다.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 각 영화가 데이터베이스에 올바르게 저장되었는지 확인합니다.
        for movie_data in self.valid_payload()['movies']:
            movie = Movie.objects.get(title=movie_data['movie']['title'])
            self.assertEqual(movie.release_year, movie_data['movie']['release_year'].split('–')[0])
            self.assertEqual(movie.score, Decimal(movie_data['movie']['score']))
            self.assertEqual(movie.summary, movie_data['movie']['summary'])
            self.assertEqual(movie.image_url, movie_data['movie']['image_url'])

            # 관련된 장르와 배우가 데이터베이스에 저장되었는지 확인합니다.
            for genre_name in movie_data['movie']['genres']:
                genre = Genre.objects.get(name=genre_name)
                self.assertIn(genre, movie.genres.all())

            for actor_name in movie_data['movie']['actors']:
                actor = Actor.objects.get(name=actor_name)
                self.assertIn(actor, movie.actors.all())

            # 랭킹 정보도 제대로 저장되었는지 확인합니다.
            ranking = Ranking.objects.get(movie=movie)
            self.assertEqual(ranking.rank, movie_data['rank'])
            self.assertEqual(ranking.country.code, movie_data['country_code'])

    def test_bulk_insert_invalid_movies(self):
        # 잘못된 데이터로 요청을 보내서 400 Bad Request 응답을 받는지 확인합니다.
        invalid_payload = {
            "movies": [
                {
                    "country_code": "KR",
                    "movie": {
                        "title": "",  # 잘못된 제목 (빈 문자열)
                        "release_year": "2021",
                        "score": "8.0",
                        "summary": "Description",
                        "image_url": "https://example.com/image.jpg",
                        "genres": ["Action"],
                        "actors": ["Actor"]
                    },
                    "rank": 1
                }
            ]
        }

        response = self.client.post(self.url, invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
"""
from django.test import TestCase
from rest_framework.test import APIClient

class BulkInsertRankingTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/bulk-insert-ranking/'
        self.payload = {
            "movies": [
                {
                    "country_code": "KR",
                    "rank": 1,
                    "movie": {
                        "title": "오징어 게임",
                        "release_year": "2021–2025",
                        "score": 8.0,
                        "summary": "Hundreds of cash-strapped players accept a strange invitation...",
                        "image_url": "http://example.com/squid-game.jpg",
                        "genres": ["Action", "Drama", "Mystery"],
                        "actors": ["Lee Jung-jae", "Park Hae-soo", "Nandito Hidayattullah Putra"]
                    }
                }
            ]
        }

    def test_bulk_insert_ranking(self):
        response = self.client.post(self.url, self.payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Movie.objects.count(), 1)
        self.assertEqual(Country.objects.count(), 1)
