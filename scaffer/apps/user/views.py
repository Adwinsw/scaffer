from rest_framework import viewsets
from user.serializers import UserSerializer,User

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    
    permission_classes = []
    queryset = User.objects.all()
    serializer_class = UserSerializer