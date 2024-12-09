from django.urls import path
from .views import CrawlMoviesView  # 앞에서 작성한 CrawlMoviesView import

urlpatterns = [
    path('api/crawl_movies/', CrawlMoviesView.as_view(), name='crawl_movies'),
]