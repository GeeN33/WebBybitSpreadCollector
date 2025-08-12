from rest_framework import serializers

from gateio.models import BarSpreadGateio, PairGateio


class BarSpreadGateioSerializer(serializers.ModelSerializer):
    class Meta:
        model = BarSpreadGateio
        fields = '__all__'


class PairGateioSerializer(serializers.ModelSerializer):
    class Meta:
        model = PairGateio
        fields = '__all__'