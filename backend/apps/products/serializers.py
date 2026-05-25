from rest_framework import serializers
from .models import Categoria, Producto

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    # Esto permite ver el nombre de la categoría en lugar de solo el ID al hacer un GET
    categoria_nombre = serializers.ReadOnlyField(source='categoria.nombre')

    # Devuelve la URL absoluta de Cloudinary (o local en desarrollo)
    imagen_url = serializers.SerializerMethodField()

    class Meta:
        model = Producto
        fields = [
            'id', 'nombre', 'descripcion', 'precio',
            'stock', 'disponible', 'categoria', 'categoria_nombre',
            'imagen', 'imagen_url', 'creado_en'
        ]

    def get_imagen_url(self, obj):
        """
        Devuelve la URL completa de la imagen:
        - Si está en Cloudinary: devuelve la URL de Cloudinary directamente.
        - Si es local (desarrollo): construye la URL absoluta con el request.
        - Si no hay imagen: devuelve None.
        """
        if not obj.imagen:
            return None
        url = obj.imagen.url
        # Las URLs de Cloudinary ya son absolutas (https://res.cloudinary.com/...)
        if url.startswith('http'):
            return url
        # URL local: construir URL absoluta usando el request
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(url)
        return url