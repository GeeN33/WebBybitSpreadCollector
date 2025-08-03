from rest_framework import serializers

from collector.models import BarSpread


class BarSpreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = BarSpread
        fields = '__all__'