from django.urls import path
from .views import CreateOrderView, OrderHistoryView, OrderQueueView, UpdateOrderStatusView, MyOrdersView

urlpatterns = [
    path('',          CreateOrderView.as_view()),       # POST  /api/orders/
    path('queue/',    OrderQueueView.as_view()),         # GET   /api/orders/queue/
    path('mine/',     MyOrdersView.as_view()),           # GET   /api/orders/mine/
    path('<int:pk>/', UpdateOrderStatusView.as_view()),  # PATCH /api/orders/{id}/
    path('history/', OrderHistoryView.as_view()),  # GET /api/orders/history/
]