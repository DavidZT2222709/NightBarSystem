# apps/stats/serializers.py
from rest_framework import serializers
from .models import ReporteDiario

class ReporteDiarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReporteDiario
        fields = '__all__'