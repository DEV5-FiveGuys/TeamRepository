from django.contrib import admin
from django.urls import path
from .views import BulkInsertRankingView, GetMovieListByCountryAPIView, CrawlMoviesView
from django.urls import path
from .views import home

urlpatterns = [
    path('bulk-insert-ranking/', BulkInsertRankingView.as_view(), name='bulk-insert-ranking'),
    path('movies/<str:country_name>/', GetMovieListByCountryAPIView.as_view(), name='movies-by-country'),
    path('crawl_movies/', CrawlMoviesView.as_view(), name='crawl_movies'),
    path('', home, name='home'),  # 루트 URL에 home 뷰 연결
]