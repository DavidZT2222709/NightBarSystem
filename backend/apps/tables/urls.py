from django.urls import path
from .views import TableListView, TableUpdateView

urlpatterns = [
    path('',          TableListView.as_view()),    # GET   /api/tables/
    path('<int:pk>/', TableUpdateView.as_view()),  # PATCH /api/tables/{id}/
]