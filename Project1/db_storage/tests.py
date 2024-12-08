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
                    "country": "KR",
                    "movie": {
                        "title": "오징어 게임",
                        "release_year": "2021–2025",
                        "score": "8.0",
                        "summary": "Hundreds of cash-strapped players accept a strange invitation to compete in children's games.",
                        "image_url": "https://m.media-amazon.com/images/M/MV5BYTYzMTlmNDctNmVkNS00YzRlLWE5MjAtODdjZWRkYzRlNWVlXkEyXkFqcGc@._V1_QL75_UX72_CR0,0,72,107_.jpg",
                        "genres": ["Action", "Drama", "Mystery"],
                        "actors": ["Lee Jung-jae", "Park Hae-soo", "Nandito Hidayattullah Putra"]
                    },
                    "rank": 1
                },
                {
                    "country": "KR",
                    "movie": {
                        "title": "Mr. Peullangkeuton",
                        "release_year": "2024",
                        "score": "8.2",
                        "summary": "A man with little chance for happiness and his ex, the unhappiest bride-to-be, are forced to accompany one another on the final journey of his life.",
                        "image_url": "https://m.media-amazon.com/images/M/MV5BNzNkMzNmZjAtNTM2Ni00OGNkLTk2MzQtZWU3ZDMwNjUzYTZkXkEyXkFqcGc@._V1_QL75_UX72_CR0,0,72,107_.jpg",
                        "genres": ["Comedy", "Romance"],
                        "actors": ["Woo Do-Hwan", "Lee Yoo-mi", "Oh Jung-se"]
                    },
                    "rank": 2
                },
                {
                    "country": "KR",
                    "movie": {
                        "title": "Gisaengchung",
                        "release_year": "2019",
                        "score": "8.5",
                        "summary": "Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.",
                        "image_url": "https://m.media-amazon.com/images/M/MV5BYjk1Y2U4MjQtY2ZiNS00OWQyLWI3MmYtZWUwNmRjYWRiNWNhXkEyXkFqcGc@._V1_QL75_UX72_CR0,0,72,107_.jpg",
                        "genres": ["Drama", "Thriller"],
                        "actors": ["Bong Joon Ho", "Lee Sun-kyun", "Cho Yeo-jeong"]
                    },
                    "rank": 3
                },
                {
                    "country": "KR",
                    "movie": {
                        "title": "Oldeuboi",
                        "release_year": "2003",
                        "score": "8.3",
                        "summary": "After being kidnapped and imprisoned for fifteen years, Oh Dae-Su is released, only to find that he must track down his captor in five days.",
                        "image_url": "https://m.media-amazon.com/images/M/MV5BMTI3NTQyMzU5M15BMl5BanBnXkFtZTcwMTM2MjgyMQ@@._V1_QL75_UX72_CR0,0,72,107_.jpg",
                        "genres": ["Action", "Drama", "Mystery"],
                        "actors": ["Park Chan-wook", "Yoo Ji-tae", "Kang Hye-jeong"]
                    },
                    "rank": 4
                },
                {
                    "country": "KR",
                    "movie": {
                        "title": "Gangnam Bi-Saideu",
                        "release_year": "2024",
                        "score": "7.4",
                        "summary": "In Gangnam, Seoul, Jae-Hee knows a secret about a series of disappearances but then vanishes herself. Detective Kang, outlaw Yoon, and Prosecutor Min pursue the truth for their own reasons.",
                        "image_url": "https://m.media-amazon.com/images/M/MV5BNjgwYmJhYjgtYzJhYi00NmU5LWE1ZjEtOWRjOWJkN2M3MTU2XkEyXkFqcGc@._V1_QL75_UY107_CR1,0,72,107_.jpg",
                        "genres": ["Action", "Crime", "Drama"],
                        "actors": ["Jo Woo-jin", "Ji Chang-wook", "Ha Yoon-kyung"]
                    },
                    "rank": 5
                },
                {
                    "country": "KR",
                    "movie": {
                        "title": "Ahgassi",
                        "release_year": "2016",
                        "score": "8.1",
                        "summary": "In 1930s Korea, a girl is hired as a handmaiden to a Japanese heiress who lives a secluded life on a countryside estate.",
                        "image_url": "https://m.media-amazon.com/images/M/MV5BZjIwMjVjNmEtZGY4Ni00MjFlLTgwZTMtYTVlNWFjNTE0M2FjXkEyXkFqcGc@._V1_QL75_UY107_CR2,0,72,107_.jpg",
                        "genres": ["Drama", "Romance", "Thriller"],
                        "actors": ["Park Chan-wook", "Ha Jung-woo", "Cho Jin-woong"]
                    },
                    "rank": 6
                },
                        {
                    "country": "KR",
                    "movie": {
                        "title": "기생충",
                        "release_year": "2019",
                        "score": "8.5",
                        "summary": "Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.",
                        "image_url": "https://example.com/parasite.jpg",
                        "genres": ["Drama", "Thriller"],
                        "actors": ["Bong Joon Ho", "Song Kang-ho", "Choi Woo-shik"]
                    },
                    "rank": 1
                },
                {
                    "country": "US",
                    "movie": {
                        "title": "The Dark Knight",
                        "release_year": "2008",
                        "score": "9.0",
                        "summary": "Batman battles the Joker, a criminal mastermind who wants to plunge Gotham into anarchy.",
                        "image_url": "https://example.com/dark_knight.jpg",
                        "genres": ["Action", "Drama", "Crime"],
                        "actors": ["Christian Bale", "Heath Ledger", "Aaron Eckhart"]
                    },
                    "rank": 2
                },
                {
                    "country": "IN",
                    "movie": {
                        "title": "3 Idiots",
                        "release_year": "2009",
                        "score": "8.4",
                        "summary": "Two friends look for their long-lost companion, recounting their college days and the ways he inspired them.",
                        "image_url": "https://example.com/3idiots.jpg",
                        "genres": ["Comedy", "Drama"],
                        "actors": ["Aamir Khan", "R. Madhavan", "Sharman Joshi"]
                    },
                    "rank": 3
                },
                {
                    "country": "KR",
                    "movie": {
                        "title": "올드보이",
                        "release_year": "2003",
                        "score": "8.4",
                        "summary": "After being imprisoned for 15 years, Oh Dae-Su seeks revenge on his captor.",
                        "image_url": "https://example.com/oldboy.jpg",
                        "genres": ["Action", "Mystery", "Drama"],
                        "actors": ["Choi Min-sik", "Yoo Ji-tae", "Kang Hye-jeong"]
                    },
                    "rank": 4
                },
                {
                    "country": "US",
                    "movie": {
                        "title": "Interstellar",
                        "release_year": "2014",
                        "score": "8.6",
                        "summary": "A team of explorers travel through a wormhole in space in an attempt to save humanity.",
                        "image_url": "https://example.com/interstellar.jpg",
                        "genres": ["Sci-Fi", "Adventure", "Drama"],
                        "actors": ["Matthew McConaughey", "Anne Hathaway", "Jessica Chastain"]
                    },
                    "rank": 5
                }
            ]
        }


    def test_bulk_insert_ranking(self):
        response = self.client.post(self.url, self.payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)