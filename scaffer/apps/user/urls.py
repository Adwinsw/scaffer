from rest_framework import routers
from user.views import UserViewSet

router = routers.DefaultRouter()
router.register('member',UserViewSet,'member-user')

urlpatterns = router.urls