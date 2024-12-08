from django.contrib import admin
from django.urls import path
from .views import BulkInsertRankingView

urlpatterns = [
    path('bulk-insert-ranking/', BulkInsertRankingView.as_view(), name='bulk-insert-ranking'),
]