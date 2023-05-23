from rest_framework import routers
from scanner.views import ScannerViewSet

router = routers.DefaultRouter()
router.register('member',ScannerViewSet,'member-scanner')

urlpatterns = router.urls