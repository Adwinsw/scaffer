from rest_framework import viewsets
from asset.serializers import AssetSerializer,Asset

# Create your views here.

class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer