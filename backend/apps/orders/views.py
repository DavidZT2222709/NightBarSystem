from rest_framework import generics
from .models import Order
from .serializers import OrderSerializer, OrderStatusSerializer
from apps.users.permissions import IsMesero, IsBartender
from django.utils import timezone

class CreateOrderView(generics.CreateAPIView):
    """RF-004 al RF-007: El mesero crea y envía un pedido."""
    serializer_class   = OrderSerializer
    permission_classes = [IsMesero]

    def perform_create(self, serializer):
        serializer.save(mesero=self.request.user)


class OrderQueueView(generics.ListAPIView):
    """RF-008: El bartender ve los pedidos en orden de llegada."""
    serializer_class   = OrderSerializer
    permission_classes = [IsBartender]

    def get_queryset(self):
        queryset = self.queryset.exclude(status='delivered')
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)

        return queryset



class UpdateOrderStatusView(generics.UpdateAPIView):
    """RF-009 y RF-010: El bartender cambia el estado del pedido."""
    serializer_class   = OrderStatusSerializer
    permission_classes = [IsBartender]
    queryset           = Order.objects.all()
    http_method_names  = ['patch']


class MyOrdersView(generics.ListAPIView):
    """El mesero consulta el estado de sus pedidos activos."""
    serializer_class   = OrderSerializer
    permission_classes = [IsMesero]

    def get_queryset(self):
        return Order.objects.filter(
            mesero=self.request.user
        ).exclude(status='delivered')

class OrderHistoryView(generics.ListAPIView):
    """Pedidos entregados del día actual."""
    serializer_class   = OrderSerializer
    permission_classes = [IsMesero]

    def get_queryset(self):
        today = timezone.now().date()
        return Order.objects.filter(
            mesero=self.request.user,
            status='delivered',
            created_at__date=today
        )