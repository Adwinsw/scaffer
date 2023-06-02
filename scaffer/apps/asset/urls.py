from rest_framework import routers
from asset.views import AssetViewSet

router = routers.DefaultRouter()
router.register('member',AssetViewSet,'member-asset')

urlpatterns = router.urls