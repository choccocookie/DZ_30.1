from rest_framework.routers import SimpleRouter
from django.urls import path, include
from system.views import PaymentViewSet
from system.apps import SystemConfig

app_name = SystemConfig.name

router = SimpleRouter()
router.register("payments", PaymentViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

