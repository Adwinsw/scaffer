from rest_framework import serializers
from flow.models import Flow

class FlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flow
        fields = ['username']