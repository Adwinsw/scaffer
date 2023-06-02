from rest_framework import routers
from probe.views import ProbeViewSet

router = routers.DefaultRouter()
router.register('member',ProbeViewSet,'member-probe')

urlpatterns = router.urls