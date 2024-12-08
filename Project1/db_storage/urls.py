# db_storage/urls.py
from django.contrib import admin
from django.urls import path
from .views import BulkInsertRankingView, GetMovieListByCountryAPIView, movie_list, movie_details

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bulk-insert-ranking/', BulkInsertRankingView.as_view(), name='bulk-insert-ranking'),
    path('movies/<str:country_name>/', GetMovieListByCountryAPIView.as_view(), name='movies-by-country'),
    path('', movie_list, name='movie_list'),  # 영화 목록 페이지
    path('movie/<int:movie_id>/', movie_details, name='movie_details'),  # 영화 상세 페이지
]