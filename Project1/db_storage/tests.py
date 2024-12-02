from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Country, Genre, Actor, Movie, Ranking

class BulkInsertRankingViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('bulk-insert-ranking')  # Replace with the actual view name
        self.valid_payload = [
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
    def test_bulk_insert_multiple_movies(self):
        for payload in self.valid_payload:
            response = self.client.post(self.url, data=payload, format='json')

            print()
            print(response.data)
            print()
            
            # Check response
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data['message'], 'Bulk insert successful')

            # Verify data in the database
            country_code = payload['country_code']
            movie_data = payload['movie']
            self.assertTrue(Country.objects.filter(code=country_code).exists())
            self.assertTrue(Movie.objects.filter(title=movie_data['title']).exists())

            for genre_name in movie_data['genres']:
                self.assertTrue(Genre.objects.filter(name=genre_name).exists())

            for actor_name in movie_data['actors']:
                self.assertTrue(Actor.objects.filter(name=actor_name).exists())

            self.assertTrue(Ranking.objects.filter(rank=payload['rank']).exists())
                
    # def test_bulk_insert_duplicate_handling(self):
    #     # First insertion
    #     response1 = self.client.post(self.url, data=self.valid_payload, format='json')
    #     self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

    #     # Duplicate insertion
    #     response2 = self.client.post(self.url, data=self.valid_payload, format='json')
    #     self.assertEqual(response2.status_code, status.HTTP_201_CREATED)

    #     # Check no duplicates in database
    #     self.assertEqual(Movie.objects.filter(title="오징어 게임").count(), 1)
    #     self.assertEqual(Ranking.objects.filter(rank=1).count(), 1)

