from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Product
from .serializers import ProductSerializer

class ProductListView(generics.ListAPIView):
    """Todos los roles pueden ver el catálogo de productos."""
    serializer_class   = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Product.objects.filter(available=True)