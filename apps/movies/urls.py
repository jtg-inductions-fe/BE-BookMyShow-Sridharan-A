from rest_framework import routers

from .views import MovieViewSet

router = routers.SimpleRouter()
router.register(r"", MovieViewSet)

urlpatterns = router.urls
