from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from user.serializers import UserSerializer, GroupSerializer, UserProfile, UserGroup
from authen.backends.status import SessionAuthentication, CustomTokenAuthentication

from utils import drfapi
# Create your views here.

class UserViewSet(drfapi.MixinViewSet):
    authentication_classes = [SessionAuthentication, CustomTokenAuthentication]
    permission_classes = []

    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer

    def perform_update(self, serializer):
        group_id = self.request.data.get('groups_id', None)
        if group_id:
            group_id_list = str(group_id).split(',')
            group_queryset_list = UserGroup.objects.filter(id__in=group_id_list).all()
            serializer.validated_data['groups'] = group_queryset_list
        return super().perform_update(serializer)

class GroupViewSet(drfapi.MixinViewSet):
    authentication_classes = [SessionAuthentication, CustomTokenAuthentication]
    permission_classes = []

    queryset = UserGroup.objects.all()
    serializer_class = GroupSerializer

class UserInfoView(APIView):

    authentication_classes = [SessionAuthentication, CustomTokenAuthentication]
    permission_classes = []
    def get(self, request): 
        try:
            userinfo = request.user
            if userinfo:
                return Response({'code': 20000, 'username': userinfo.username, 'name': userinfo.name}, status=status.HTTP_200_OK)
            else:
                return Response({'code': 50012, 'message': '会话异常，不可用'}, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({'code': 50014, 'message': '会话异常，不可用， {0}'.format(ex)}, status=status.HTTP_200_OK)