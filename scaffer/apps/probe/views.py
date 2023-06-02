from rest_framework import viewsets
from probe.serializers import ProbeSerializer,Probe

# Create your views here.

class ProbeViewSet(viewsets.ModelViewSet):
    queryset = Probe.objects.all()
    serializer_class = ProbeSerializer