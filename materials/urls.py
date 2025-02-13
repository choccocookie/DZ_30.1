from rest_framework.routers import SimpleRouter

from materials.views import CourseViewSet
from materials.apps import MaterialsConfig
app_name = MaterialsConfig.name

router = SimpleRouter()
router.register("", CourseViewSet)

urlpatterns = []

urlpatterns += router.urls


