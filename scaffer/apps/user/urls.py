from django.urls import path
from rest_framework import routers
from user.views import UserViewSet, UserInfoView

router = routers.DefaultRouter()
router.register('member',UserViewSet,'member-user')

urlpatterns = [
    path('info/', UserInfoView.as_view(), name='get-user-info')
]

urlpatterns += router.urls