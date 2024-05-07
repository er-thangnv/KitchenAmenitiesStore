from rest_framework import serializers
from .models import Trademarks

class TrademarksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trademarks
        fields = ['id', 'name', 'link_info']
