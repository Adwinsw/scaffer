from rest_framework import viewsets
from flow.serializers import FlowSerializer,Flow

# Create your views here.

class FlowViewSet(viewsets.ModelViewSet):
    queryset = Flow.objects.all()
    serializer_class = FlowSerializer