from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import Sum, Count, F
from apps.orders.models import Order, OrderItem
from apps.users.permissions import IsAdmin

class DailyStatsView(APIView):
    """Estadísticas del día para el administrador."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = timezone.now().date()
        orders_today = Order.objects.filter(
            status='delivered',
            created_at__date=today
        )

        # Total de ingresos del día
        total_revenue = orders_today.annotate(
            order_total=Sum(
                F('items__quantity') * F('items__product__price')
            )
        ).aggregate(total=Sum('order_total'))['total'] or 0

        # Total de pedidos entregados
        total_orders = orders_today.count()

        # Productos más pedidos
        top_products = OrderItem.objects.filter(
            order__status='delivered',
            order__created_at__date=today
        ).values(
            name=F('product__name')
        ).annotate(
            total_quantity=Sum('quantity'),
            total_revenue=Sum(F('quantity') * F('product__price'))
        ).order_by('-total_quantity')[:5]

        # Pedidos por mesero
        orders_by_mesero = orders_today.values(
            mesero=F('mesero__username')
        ).annotate(
            total_orders=Count('id')
        ).order_by('-total_orders')

        return Response({
            'date':              str(today),
            'total_revenue':     total_revenue,
            'total_orders':      total_orders,
            'top_products':      list(top_products),
            'orders_by_mesero':  list(orders_by_mesero),
        })


class MonthlyStatsView(APIView):
    """Ingresos y pedidos agrupados por día del mes actual."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today  = timezone.now().date()
        orders = Order.objects.filter(
            status='delivered',
            created_at__year=today.year,
            created_at__month=today.month
        ).annotate(
            day=F('created_at__date')
        ).values('day').annotate(
            total_orders=Count('id'),
            total_revenue=Sum(
                F('items__quantity') * F('items__product__price')
            )
        ).order_by('day')

        return Response({
            'month':  today.month,
            'year':   today.year,
            'data':   list(orders)
        })