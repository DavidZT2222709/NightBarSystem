from rest_framework import serializers
from django.db import transaction
from .models import Pedido, DetallePedido
from apps.products.models import Producto

class DetallePedidoSerializer(serializers.ModelSerializer):
    # Campos de solo lectura para mostrar información al Bartender
    nombre_producto = serializers.ReadOnlyField(source='producto.nombre')
    subtotal = serializers.ReadOnlyField()

    class Meta:
        model = DetallePedido
        fields = ['id', 'producto', 'nombre_producto', 'cantidad', 'precio_unitario', 'subtotal']
        # El precio unitario se capturará del catálogo en el momento de la creación
        extra_kwargs = {'precio_unitario': {'read_only': True}}

class PedidoSerializer(serializers.ModelSerializer):
    # Anidamos el detalle dentro del pedido
    detalles = DetallePedidoSerializer(many=True)
    nombre_mesero = serializers.ReadOnlyField(source='mesero.nombre')
    numero_mesa = serializers.ReadOnlyField(source='mesa.numero') # Asumiendo campo 'numero' en Table
    total = serializers.ReadOnlyField(source='total_pedido')

    class Meta:
        model = Pedido
        fields = [
            'id', 'mesa', 'numero_mesa', 'mesero', 'nombre_mesero', 
            'estado', 'detalles', 'total', 'creado_en'
        ]
        read_only_fields = ['mesero', 'estado', 'creado_en']

    def create(self, validated_data):
        """
        Lógica personalizada para crear el Pedido y sus detalles en una sola transacción.
        """
        detalles_data = validated_data.pop('detalles')
        
        # Usamos un bloque atómico para asegurar la integridad de los datos
        with transaction.atomic():
            # 1. Crear el Pedido principal
            pedido = Pedido.objects.create(**validated_data)
            
            # 2. Crear cada detalle capturando el precio actual del producto
            for detalle in detalles_data:
                producto = detalle['producto']
                
                # RF-006: Validación de stock o disponibilidad (opcional)
                if not producto.disponible:
                    raise serializers.ValidationError(
                        f"El producto {producto.nombre} no está disponible actualmente."
                    )

                DetallePedido.objects.create(
                    pedido=pedido,
                    producto=producto,
                    cantidad=detalle['cantidad'],
                    # Capturamos el precio del catálogo para que el historial sea inalterable
                    precio_unitario=producto.precio 
                )
            
        return pedido