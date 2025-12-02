from rest_framework import serializers
from .models import Retiro

class RetiroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Retiro
        fields = ['id', 'producto', 'cantidad', 'operario', 'timestamp']
        read_only_fields = ['id', 'timestamp']
    
    def validate_cantidad(self, value):
        if value <= 0:
            raise serializers.ValidationError("La cantidad debe ser mayor a 0")
        return value
    
    def validate_producto(self, value):
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("El producto no puede estar vacío")
        return value.strip()
    
    def validate_operario(self, value):
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("El operario no puede estar vacío")
        return value.strip()