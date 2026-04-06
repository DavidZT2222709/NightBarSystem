from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model  = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity']

    def validate_product(self, product):
        if not product.available:
            raise serializers.ValidationError(
                f"El producto '{product.name}' no está disponible."
            )
        return product

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "La cantidad debe ser mayor a cero."
            )
        return value


class OrderSerializer(serializers.ModelSerializer):
    items        = OrderItemSerializer(many=True)
    mesero       = serializers.StringRelatedField(read_only=True)
    table_number = serializers.IntegerField(source='table.number', read_only=True)

    class Meta:
        model  = Order
        fields = ['id', 'mesero', 'table', 'table_number', 'status', 'created_at', 'items']
        read_only_fields = ['status', 'created_at', 'mesero']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item in items_data:
            OrderItem.objects.create(order=order, **item)
        return order


class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Order
        fields = ['status']