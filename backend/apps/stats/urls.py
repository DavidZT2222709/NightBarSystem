from django.urls import path
from .views import DailyStatsView, MonthlyStatsView

urlpatterns = [
    path('daily/',   DailyStatsView.as_view()),    # GET /api/stats/daily/
    path('monthly/', MonthlyStatsView.as_view()),  # GET /api/stats/monthly/
]