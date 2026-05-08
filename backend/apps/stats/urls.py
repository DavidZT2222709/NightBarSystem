# apps/stats/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReporteDiarioViewSet

router = DefaultRouter()
router.register(r'reportes', ReporteDiarioViewSet, basename='reportes')

urlpatterns = [
    path('', include(router.urls)),
]