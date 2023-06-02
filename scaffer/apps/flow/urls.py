from rest_framework import routers
from flow.views import FlowViewSet

router = routers.DefaultRouter()
router.register('member',FlowViewSet,'member-flow')

urlpatterns = router.urls