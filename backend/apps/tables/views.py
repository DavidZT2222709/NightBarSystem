from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Table
from .serializers import TableSerializer

class TableListView(generics.ListAPIView):
    """Todos los roles pueden ver las mesas disponibles."""
    serializer_class   = TableSerializer
    permission_classes = [IsAuthenticated]
    queryset           = Table.objects.all().order_by('number')

class TableUpdateView(generics.UpdateAPIView):
    """Actualiza el estado de una mesa (disponible / ocupada)."""
    serializer_class   = TableSerializer
    permission_classes = [IsAuthenticated]
    queryset           = Table.objects.all()
    http_method_names  = ['patch']