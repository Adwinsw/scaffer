from rest_framework import serializers
from probe.models import Probe

class ProbeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Probe
        fields = ['username']