from rest_framework import serializers

from binans.models import BarSpreadBinans, InstrumentBinans


class BarSpreadBinansSerializer(serializers.ModelSerializer):
    class Meta:
        model = BarSpreadBinans
        fields = '__all__'


class InstrumentBinansSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstrumentBinans
        fields = '__all__'