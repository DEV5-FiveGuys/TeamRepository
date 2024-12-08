from django.contrib import admin
from django.urls import path
from .views import BulkInsertRankingView, GetMovieListByCountryAPIView

urlpatterns = [
    path('bulk-insert-ranking/', BulkInsertRankingView.as_view(), name='bulk-insert-ranking'),
    path('movies/<str:country_name>/', GetMovieListByCountryAPIView.as_view(), name='movies-by-country')
]