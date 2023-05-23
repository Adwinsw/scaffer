from rest_framework import viewsets
from scanner.serializers import ScannerSerializer,Scanner

# Create your views here.

class ScannerViewSet(viewsets.ModelViewSet):
    queryset = Scanner.objects.all()
    serializer_class = ScannerSerializer