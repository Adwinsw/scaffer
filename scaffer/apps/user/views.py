from rest_framework import viewsets
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from user.serializers import UserSerializer,UserProfile
from authen.backends.status import SessionAuthentication


# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = []

    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer


class UserInfoView(APIView):

    authentication_classes = [SessionAuthentication]    
    permission_classes = []
    def get(self, request): 
        try:
            userinfo = request.user
            if userinfo:
                return Response({'code': 20000, 'username': userinfo.username, 'name': userinfo.name}, status=status.HTTP_200_OK)
            else:
                return Response({'code': 50012, 'message': '会话异常，不可用'}, status=status.HTTP_200_OK)
        except Exception as ex:
            print(ex)
            return Response({'code': 500014, 'message': '会话异常，不可用， {0}'.format(ex)}, status=status.HTTP_200_OK)