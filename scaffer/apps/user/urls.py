from django.urls import path
from rest_framework import routers
from user.views import UserViewSet, GroupViewSet, UserInfoView

router = routers.DefaultRouter()
router.register(r'user_member',UserViewSet,'member-user')
router.register(r'group_member',GroupViewSet,'member-group')

urlpatterns = [
    path('info/', UserInfoView.as_view(), name='get-user-info')
]

urlpatterns += router.urls